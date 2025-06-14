"""
Controller para gerenciamento de Bombonas
"""

import csv
import os
import unicodedata
from datetime import datetime
from typing import List
from dao.interfaces.bombona_dao_interface import BombonaDAOInterface
from dao.interfaces.responsavel_dao_interface import ResponsavelDAOInterface
from factory.bombona_factory import BombonaFactory
from models.bombona import Bombona

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None  # Para tratar caso não esteja instalado


class BombonaController:
    """
    Controller responsável pela lógica de negócio relacionada às bombonas.
    Atua como intermediário entre a camada de apresentação e os DAOs.
    Utiliza as interfaces dos DAOs para garantir baixo acoplamento.
    """

    def __init__(self):
        """
        Inicializa o controller com suas próprias dependências.
        O controller é autônomo e trabalha apenas com interfaces.
        """

        # Import dinâmico das implementações (mantém baixo acoplamento)
        from dao.bombona_dao import BombonaDAO
        from dao.responsavel_dao import ResponsavelDAO
        
        # Atribui às interfaces (polimorfismo)
        self._bombona_dao: BombonaDAOInterface = BombonaDAO()
        self._responsavel_dao: ResponsavelDAOInterface = ResponsavelDAO()
        self._bombona_factory = BombonaFactory()

    def cadastrar_bombona(self, codigo: str, volume: float, tipo_residuo: str, cpf: str) -> bool:
        """ Cadastra uma nova bombona com responsável vinculado. """

        try:
            # Verifica se o código já existe ANTES de processar
            if self._bombona_dao.existe_codigo(codigo):
                raise ValueError(f"Já existe uma bombona com o código {codigo}")

            # Factory cria bombona sem responsável (validação dos dados próprios)
            bombona_temp = self._bombona_factory.criar_bombona(codigo, volume, tipo_residuo)

            # Controller valida e busca responsável (acesso ao BD)
            cpf_formatado = self._normalizar_cpf(cpf)
            responsavel = self._responsavel_dao.buscar_por_cpf(cpf_formatado)
            
            if not responsavel:
                raise ValueError(f"Responsável com CPF {cpf} não encontrado")

            # Controller cria bombona final com responsável vinculado
            # bombona_final = Bombona(
            #     codigo=bombona_temp.get_codigo(),
            #     volume=bombona_temp.get_volume(),
            #     tipo_residuo=bombona_temp.get_tipo_residuo(),
            #     responsavel=responsavel
            # )

            bombona_temp.set_responsavel(responsavel)

            # Salva a bombona com responsável vinculado
            self._bombona_dao.salvar(bombona_temp)

            return True

        except Exception as e:
            print(f"Erro ao cadastrar bombona: {e}")
            raise

    def listar_bombonas(self) -> List[Bombona]:
        """ Lista todas as bombonas cadastradas com as referências aos responsáveis resolvidas. """

        try:
            # bombonas = self._bombona_dao.listar_todas()
            # return self._resolver_referencias_responsaveis(bombonas)
            return self._bombona_dao.listar_todas()
        except Exception as e:
            print(f"Erro ao listar bombonas: {e}")
            return []

    def remover_bombona(self, codigo: str) -> bool:
        """ Remove uma bombona pelo código. """

        try:
            bombona = self._bombona_dao.buscar_por_codigo(codigo)
            if not bombona:
                raise ValueError(f"Bombona com código {codigo} não encontrada")

            self._bombona_dao.remover(bombona)
            return True

        except Exception as e:
            print(f"Erro ao remover bombona: {e}")
            raise

    def editar_bombona(self, codigo: str, novo_volume: float, novo_tipo_residuo: str, cpf_responsavel: str) -> bool:
        """ Edita os dados de uma bombona existente. """

        try:
            # Busca a bombona existente
            bombona = self._bombona_dao.buscar_por_codigo(codigo)
            if not bombona:
                raise ValueError(f"Bombona com código {codigo} não encontrada")

            # Factory valida apenas os dados da bombona
            bombona_temp = self._bombona_factory.criar_bombona(codigo, novo_volume, novo_tipo_residuo)

            # Controller valida e busca responsável
            cpf_formatado = self._normalizar_cpf(cpf_responsavel)
            responsavel = self._responsavel_dao.buscar_por_cpf(cpf_formatado)
            
            if not responsavel:
                raise ValueError(f"Responsável com CPF {cpf_responsavel} não encontrado")

            # Controller cria bombona final com responsável vinculado
            bombona_atualizada = Bombona(
                codigo=bombona_temp.get_codigo(),
                volume=bombona_temp.get_volume(),
                tipo_residuo=bombona_temp.get_tipo_residuo(),
                responsavel=responsavel
            )

            # Atualiza a bombona
            self._bombona_dao.atualizar(bombona_atualizada)

            return True

        except Exception as e:
            print(f"Erro ao editar bombona: {e}")
            raise

    def buscar_bombonas_por_cpf_responsavel(self, cpf: str) -> List[Bombona]:
        """ Busca bombonas por CPF do responsável com as referências resolvidas. """

        try:
            cpf_formatado = self._normalizar_cpf(cpf)
            # bombonas = self._bombona_dao.buscar_por_responsavel(cpf_formatado)
            # return self._resolver_referencias_responsaveis(bombonas)
            return self._bombona_dao.buscar_por_responsavel(cpf_formatado)
        except Exception as e:
            print(f"Erro ao buscar bombonas por responsável: {e}")
            return []

    def gerar_relatorio(self, bombonas_filtradas: List[Bombona] = None, arquivo: str = None, filtros_ativos: list = None, formato: str = "csv") -> str:
        """ Gera relatório das bombonas em formato especificado. """

        try:
            # Se não passou bombonas, usa todas
            if bombonas_filtradas is None:
                bombonas_filtradas = self.listar_bombonas()
            
            if formato.lower() == "csv":
                return self._gerar_csv(bombonas_filtradas, arquivo, filtros_ativos)
            elif formato.lower() == "pdf":
                if not arquivo:
                    raise ValueError("Caminho do arquivo é obrigatório para PDF")
                return self._gerar_pdf(bombonas_filtradas, arquivo, filtros_ativos)
            else:
                raise ValueError("Formatos suportados: 'csv' ou 'pdf'")

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            raise
    
    def _gerar_csv(self, bombonas: List[Bombona], arquivo: str = None, filtros_ativos: list = None) -> str:
        """ Gera relatório CSV das bombonas. """

        # Define arquivo se não especificado
        if not arquivo:
            nome_arquivo = "relatorio_bombonas_filtradas.csv" if filtros_ativos else "relatorio_bombonas.csv"
            arquivo = f"data/{nome_arquivo}"
        
        # Cria diretório se necessário
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho com filtros se houver
            if filtros_ativos:
                writer.writerow([f'# Filtros aplicados: {"; ".join(filtros_ativos)}'])
                writer.writerow([f'# Total de bombonas encontradas: {len(bombonas)}'])
                writer.writerow([])  # Linha vazia
            
            # Cabeçalho da tabela
            writer.writerow(['Código', 'Volume (L)', 'Tipo Resíduo', 'Responsável', 'CPF', 'Setor'])
            
            # Dados
            for bombona in bombonas:
                responsavel = bombona.get_responsavel()
                writer.writerow([
                    bombona.get_codigo(),
                    bombona.get_volume(),
                    bombona.get_tipo_residuo(),
                    responsavel.get_nome() if responsavel else 'N/A',
                    responsavel.get_cpf() if responsavel else 'N/A',
                    responsavel.get_setor() if responsavel else 'N/A'
                ])
        
        return arquivo
    
    def _gerar_pdf(self, bombonas: List[Bombona], arquivo: str, filtros_ativos: list = None) -> str:
        """ Gera relatório PDF das bombonas. """

        if FPDF is None:
            raise ImportError("Biblioteca FPDF não encontrada. Instale com: pip install fpdf2")
        
        def sanitizar_texto(texto):
            if not texto:
                return texto
            nfd = unicodedata.normalize('NFD', texto)
            return nfd.encode('ascii', 'ignore').decode('ascii')
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Título
        titulo = "RELATORIO DE BOMBONAS FILTRADAS" if filtros_ativos else "RELATORIO COMPLETO DE BOMBONAS"
        pdf.cell(0, 10, titulo, ln=True, align='C')
        pdf.ln(5)
        
        # Filtros (se houver)
        if filtros_ativos:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, "Filtros aplicados:", ln=True)
            pdf.set_font('Arial', '', 10)
            for filtro in filtros_ativos:
                filtro_limpo = sanitizar_texto(filtro)
                pdf.cell(0, 6, f"  - {filtro_limpo}", ln=True)
            pdf.ln(5)
        
        # Total
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f"Total de bombonas: {len(bombonas)}", ln=True)
        pdf.ln(5)
        
        # Cabeçalho da tabela
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(30, 8, 'Codigo', 1, 0, 'C')
        pdf.cell(25, 8, 'Volume (L)', 1, 0, 'C')
        pdf.cell(35, 8, 'Tipo Residuo', 1, 0, 'C')
        pdf.cell(60, 8, 'Responsavel', 1, 0, 'C')
        pdf.cell(40, 8, 'Setor', 1, 1, 'C')
        
        # Dados
        pdf.set_font('Arial', '', 9)
        for bombona in bombonas:
            resp = bombona.get_responsavel()
            
            # Sanitizar textos
            codigo_limpo = sanitizar_texto(bombona.get_codigo())
            tipo_limpo = sanitizar_texto(bombona.get_tipo_residuo())
            nome_resp = sanitizar_texto(resp.get_nome()) if resp else 'N/A'
            setor_resp = sanitizar_texto(resp.get_setor()) if resp else 'N/A'
            
            # Truncar se necessário
            nome_resp = (nome_resp[:25] + "...") if len(nome_resp) > 25 else nome_resp
            setor_resp = (setor_resp[:18] + "...") if len(setor_resp) > 18 else setor_resp
            
            pdf.cell(30, 6, codigo_limpo, 1, 0, 'C')
            pdf.cell(25, 6, f"{bombona.get_volume():.1f}", 1, 0, 'C')
            pdf.cell(35, 6, tipo_limpo, 1, 0, 'C')
            pdf.cell(60, 6, nome_resp, 1, 0, 'L')
            pdf.cell(40, 6, setor_resp, 1, 1, 'L')
            
            # Nova página se necessário
            if pdf.get_y() > 250:
                pdf.add_page()
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(30, 8, 'Codigo', 1, 0, 'C')
                pdf.cell(25, 8, 'Volume (L)', 1, 0, 'C')
                pdf.cell(35, 8, 'Tipo Residuo', 1, 0, 'C')
                pdf.cell(60, 8, 'Responsavel', 1, 0, 'C')
                pdf.cell(40, 8, 'Setor', 1, 1, 'C')
                pdf.set_font('Arial', '', 9)
        
        # Rodapé
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 8)
        data_geracao = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
        pdf.cell(0, 6, f"Relatorio gerado em {data_geracao}", ln=True, align='L')
        
        pdf.output(arquivo)
        return arquivo

    def _normalizar_cpf(self, cpf: str) -> str:
        """ Valida e formata o CPF removendo caracteres não numéricos. """

        import re
        if not cpf:
            raise ValueError("CPF não pode ser vazio")

        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r'\D', '', cpf)

        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")

        return cpf_limpo

    def get_tipos_residuos_validos(self) -> List[str]:
        """ Retorna os tipos de resíduos válidos. """

        return self._bombona_factory.get_tipos_residuos_validos()

    def filtrar_bombonas_por_setor(self, setor: str) -> List[Bombona]:
        """ Filtra bombonas por setor do responsável. """

        try:
            bombonas = self.listar_bombonas()
            bombonas_filtradas = []

            for bombona in bombonas:
                responsavel = bombona.get_responsavel()
                if responsavel and responsavel.get_setor() == setor:
                    bombonas_filtradas.append(bombona)

            return bombonas_filtradas

        except Exception as e:
            print(f"Erro ao filtrar bombonas por setor: {e}")
            return []

    def filtrar_bombonas_por_tipo_residuo(self, tipo_residuo: str) -> List[Bombona]:
        """ Filtra bombonas por tipo de resíduo. """

        try:
            bombonas = self.listar_bombonas()
            bombonas_filtradas = []

            for bombona in bombonas:
                if bombona.get_tipo_residuo() == tipo_residuo:
                    bombonas_filtradas.append(bombona)

            return bombonas_filtradas

        except Exception as e:
            print(f"Erro ao filtrar bombonas por tipo: {e}")
            return []
        



    # def _resolver_referencias_responsaveis(self, bombonas: List[Bombona]) -> List[Bombona]:
    #     """ Resolve as referências aos responsáveis para uma lista de bombonas. """

    #     bombonas_resolvidas = []

    #     for bombona in bombonas:
    #         # Se a bombona já tem o responsável carregado, mantém
    #         if bombona.get_responsavel():
    #             bombonas_resolvidas.append(bombona)
    #             continue

    #         # Se tem o CPF armazenado temporariamente, resolve a referência
    #         if hasattr(bombona, '_cpf_responsavel') and bombona._cpf_responsavel:
    #             responsavel = self._responsavel_dao.buscar_por_cpf(bombona._cpf_responsavel)
    #             if responsavel:
    #                 # Cria uma nova bombona com o responsável resolvido
    #                 bombona_resolvida = Bombona(
    #                     codigo=bombona.get_codigo(),
    #                     volume=bombona.get_volume(),
    #                     tipo_residuo=bombona.get_tipo_residuo(),
    #                     responsavel=responsavel
    #                 )
    #                 bombonas_resolvidas.append(bombona_resolvida)
    #             else:
    #                 # Mantém a bombona original se não encontrar o responsável
    #                 bombonas_resolvidas.append(bombona)
    #         else:
    #             # Mantém a bombona original se não tem CPF
    #             bombonas_resolvidas.append(bombona)

    #     return bombonas_resolvidas