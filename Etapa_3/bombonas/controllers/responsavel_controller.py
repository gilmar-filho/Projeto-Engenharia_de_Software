"""
Controller para gerenciamento de Responsáveis
"""
import unicodedata
import csv
import os
from datetime import datetime
from typing import List, Optional
from dao.interfaces.responsavel_dao_interface import ResponsavelDAOInterface
from dao.interfaces.bombona_dao_interface import BombonaDAOInterface
from factory.responsavel_factory import ResponsavelFactory
from models.responsavel import Responsavel

try: # Teste para garantir que o FPDF está instalado
    from fpdf import FPDF
except ImportError:
    FPDF = None

class ResponsavelController:
    """
    Controller responsável pela lógica de negócio relacionada aos responsáveis.
    Atua como intermediário entre a camada de apresentação e os DAOs.
    Utiliza as interfaces dos DAOs para garantir baixo acoplamento.
    """

    def __init__(self):
        """
        Inicializa o controller com suas próprias dependências.
        O controller é autônomo e trabalha apenas com interfaces.
        """

        # Import dinâmico das implementações (mantém baixo acoplamento)
        from dao.responsavel_dao import ResponsavelDAO
        from dao.bombona_dao import BombonaDAO
        
        # Atribui às interfaces (polimorfismo)
        self._responsavel_dao: ResponsavelDAOInterface = ResponsavelDAO()
        self._bombona_dao: BombonaDAOInterface = BombonaDAO()
        self._responsavel_factory = ResponsavelFactory()
    
    def cadastrar_responsavel(self, cpf: str, nome: str, telefone: str, setor: str) -> bool:
        """ Cadastra um novo responsável. """

        try:
            # Verifica se o CPF já existe usando a factory para validar/formatar
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            if self._responsavel_dao.existe_cpf(cpf_formatado):
                raise ValueError(f"Já existe um responsável com o CPF {cpf}")
            
            # Cria o responsável usando a factory
            responsavel = self._responsavel_factory.criar_responsavel(cpf, nome, telefone, setor)
            
            # Salva o responsável
            self._responsavel_dao.salvar(responsavel)
            
            return True
            
        except Exception as e:
            print(f"Erro ao cadastrar responsável: {e}")
            raise
    
    def listar_responsaveis(self) -> List[Responsavel]:
        """ Lista todos os responsáveis cadastrados. """

        try:
            return self._responsavel_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar responsáveis: {e}")
            return []
    
    def buscar_responsavel(self, cpf: str) -> Optional[Responsavel]:
        """ Busca um responsável pelo CPF. """

        try:
            cpf = str(cpf)
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            return self._responsavel_dao.buscar_por_cpf(cpf_formatado)
        except Exception as e:
            print(f"Erro ao buscar responsável: {e}")
            return None
    
    def remover_responsavel(self, cpf: str) -> bool:
        """ Remove um responsável pelo CPF. """

        try:
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            
            # Busca o responsável
            responsavel = self._responsavel_dao.buscar_por_cpf(cpf_formatado)
            if not responsavel:
                raise ValueError(f"Responsável com CPF {cpf} não encontrado")
            
            # Verifica se o responsável possui bombonas
            bombonas_responsavel = self._bombona_dao.buscar_por_responsavel(cpf_formatado)
            if bombonas_responsavel:
                codigos_bombonas = []
                for bombona in bombonas_responsavel:
                    codigos_bombonas.append(bombona.get_codigo())
                
                raise ValueError(f"Não é possível remover o responsável. "
                               f"Ele possui {len(bombonas_responsavel)} bombona(s) cadastrada(s): "
                               f"{', '.join(codigos_bombonas)}")
            
            # Remove o responsável
            self._responsavel_dao.remover(responsavel)
            return True
            
        except Exception as e:
            print(f"Erro ao remover responsável: {e}")
            raise
    
    def editar_responsavel(self, cpf: str, novo_nome: str, novo_telefone: str, novo_setor: str) -> bool:
        """ Edita os dados de um responsável existente. """

        try:
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            
            # Busca o responsável existente
            responsavel = self._responsavel_dao.buscar_por_cpf(cpf_formatado)
            if not responsavel:
                raise ValueError(f"Responsável com CPF {cpf} não encontrado")
            
            # Cria um novo responsável com os dados atualizados (para validar)
            novo_responsavel = self._responsavel_factory.criar_responsavel(
                cpf_formatado, novo_nome, novo_telefone, novo_setor
            )
            
            # Atualiza o responsável
            self._responsavel_dao.atualizar(novo_responsavel)
            
            return True
            
        except Exception as e:
            print(f"Erro ao editar responsável: {e}")
            raise
            
    def validar_cpf_existe(self, cpf: str) -> bool:
        """ Verifica se um CPF já está cadastrado. """

        try:
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            return self._responsavel_dao.existe_cpf(cpf_formatado)
        except:
            return False
    
    def obter_setores_disponiveis(self) -> List[str]:
        """ Retorna lista de setores únicos dos responsáveis cadastrados. """

        try:
            responsaveis = self.listar_responsaveis()
            setores = set()
            
            for responsavel in responsaveis:
                setores.add(responsavel.get_setor())
            
            return sorted(list(setores))
            
        except Exception as e:
            print(f"Erro ao obter setores: {e}")
            return []

    def filtrar_responsaveis_por_setor(self, setor: str) -> List[Responsavel]:
        """ Filtra responsáveis por setor. """

        try:
            responsaveis = self.listar_responsaveis()
            responsaveis_filtrados = []
            
            for responsavel in responsaveis:
                if responsavel.get_setor() == setor:
                    responsaveis_filtrados.append(responsavel)
            
            return responsaveis_filtrados
            
        except Exception as e:
            print(f"Erro ao filtrar responsáveis por setor: {e}")
            return []
        
    def gerar_relatorio(self, responsaveis: List[Responsavel] = None, arquivo: str = None, formato: str = "csv") -> str:
        """ Gera relatório dos responsáveis em formato especificado. """

        try:
            # Se não passou responsáveis, usa todos
            if responsaveis is None:
                responsaveis = self.listar_responsaveis()

            if formato.lower() == "csv":
                return self._gerar_csv(responsaveis, arquivo)
            elif formato.lower() == "pdf":
                if not arquivo:
                    raise ValueError("Caminho do arquivo é obrigatório para PDF")
                return self._gerar_pdf(responsaveis, arquivo)
            else:
                raise ValueError("Formatos suportados: 'csv' ou 'pdf'")

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            raise
    
    def _gerar_csv(self, responsaveis: List[Responsavel], arquivo: str = None) -> str:
        """ Gera relatório CSV de responsáveis. """

        # Define arquivo se não especificado
        if not arquivo:
            arquivo = "data/relatorio_responsaveis.csv"
        
        # Cria diretório se necessário
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)

        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nome', 'CPF', 'Telefone', 'Setor', 'Qtd_Bombonas'])
            
            for resp in responsaveis:
                bombonas = self._bombona_dao.buscar_por_responsavel(resp.get_cpf())
                writer.writerow([
                    resp.get_nome(),
                    resp.get_cpf(),
                    resp.get_telefone(),
                    resp.get_setor(),
                    len(bombonas)
                ])

        return arquivo
    
    def _gerar_pdf(self, responsaveis: List[Responsavel], arquivo: str) -> str:
        """ Gera relatório PDF de responsáveis. """

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
        pdf.cell(0, 10, "RELATORIO COMPLETO DE RESPONSAVEIS", ln=True, align='C')
        pdf.ln(5)
        
        # Total
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f"Total de responsaveis: {len(responsaveis)}", ln=True)
        pdf.ln(5)
        
        # Cabeçalho da tabela
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(50, 8, 'Nome', 1, 0, 'C')
        pdf.cell(35, 8, 'CPF', 1, 0, 'C')
        pdf.cell(35, 8, 'Telefone', 1, 0, 'C')
        pdf.cell(35, 8, 'Setor', 1, 0, 'C')
        pdf.cell(25, 8, 'Bombonas', 1, 1, 'C')
        
        # Dados
        pdf.set_font('Arial', '', 9)
        for resp in responsaveis:
            bombonas = self._bombona_dao.buscar_por_responsavel(resp.get_cpf())
            
            # Sanitizar textos
            nome_limpo = sanitizar_texto(resp.get_nome())
            setor_limpo = sanitizar_texto(resp.get_setor())
            
            # Truncar se necessário
            nome_limpo = (nome_limpo[:22] + "...") if len(nome_limpo) > 22 else nome_limpo
            setor_limpo = (setor_limpo[:15] + "...") if len(setor_limpo) > 15 else setor_limpo
            
            # Formatar CPF e telefone
            cpf = resp.get_cpf()
            cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            telefone = resp.get_telefone()
            if len(telefone) == 11:
                tel_formatado = f"({telefone[:2]}) {telefone[2]} {telefone[3:7]}-{telefone[7:]}"
            elif len(telefone) == 10:
                tel_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
            else:
                tel_formatado = telefone
            
            pdf.cell(50, 6, nome_limpo, 1, 0, 'L')
            pdf.cell(35, 6, cpf_formatado, 1, 0, 'C')
            pdf.cell(35, 6, tel_formatado, 1, 0, 'C')
            pdf.cell(35, 6, setor_limpo, 1, 0, 'L')
            pdf.cell(25, 6, str(len(bombonas)), 1, 1, 'C')
            
            # Nova página se necessário
            if pdf.get_y() > 250:
                pdf.add_page()
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(50, 8, 'Nome', 1, 0, 'C')
                pdf.cell(35, 8, 'CPF', 1, 0, 'C')
                pdf.cell(35, 8, 'Telefone', 1, 0, 'C')
                pdf.cell(35, 8, 'Setor', 1, 0, 'C')
                pdf.cell(25, 8, 'Bombonas', 1, 1, 'C')
                pdf.set_font('Arial', '', 9)
        
        # Rodapé
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 8)
        data_geracao = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
        pdf.cell(0, 6, f"Relatorio gerado em {data_geracao}", ln=True, align='L')
        
        pdf.output(arquivo)
        return arquivo
    