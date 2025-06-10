"""
Controller para gerenciamento de Responsáveis
"""
import unicodedata
from datetime import datetime
from typing import List, Optional
from dao.interfaces.responsavel_dao_interface import ResponsavelDAOInterface
from dao.interfaces.bombona_dao_interface import BombonaDAOInterface
from factory.responsavel_factory import ResponsavelFactory
from models.responsavel import Responsavel

class ResponsavelController:
    """
    Controller responsável pela lógica de negócio relacionada aos responsáveis.
    Atua como intermediário entre a camada de apresentação e os DAOs.
    Utiliza as interfaces dos DAOs para garantir baixo acoplamento.
    """
    
    def __init__(self, responsavel_dao: ResponsavelDAOInterface, bombona_dao: BombonaDAOInterface):
        """
        Inicializa o controller.
        
        Args:
            responsavel_dao (ResponsavelDAOInterface): Interface do DAO para responsáveis
            bombona_dao (BombonaDAOInterface): Interface do DAO para bombonas
        """
        self._responsavel_dao = responsavel_dao
        self._bombona_dao = bombona_dao
        self._responsavel_factory = ResponsavelFactory()
    
    def cadastrar_responsavel(self, cpf: str, nome: str, telefone: str, setor: str) -> bool:
        """
        Cadastra um novo responsável.
        
        Args:
            cpf (str): CPF do responsável
            nome (str): Nome completo
            telefone (str): Telefone de contato
            setor (str): Setor de trabalho
            
        Returns:
            bool: True se cadastrou com sucesso, False caso contrário
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
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
        """
        Lista todos os responsáveis cadastrados.
        
        Returns:
            List[Responsavel]: Lista de responsáveis
        """
        try:
            return self._responsavel_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar responsáveis: {e}")
            return []
    
    def buscar_responsavel(self, cpf: str) -> Optional[Responsavel]:
        """
        Busca um responsável pelo CPF.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            Optional[Responsavel]: Responsável encontrado ou None
        """
        try:
            cpf = str(cpf)
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            return self._responsavel_dao.buscar_por_cpf(cpf_formatado)
        except Exception as e:
            print(f"Erro ao buscar responsável: {e}")
            return None
    
    def remover_responsavel(self, cpf: str) -> bool:
        """
        Remove um responsável pelo CPF.
        
        Args:
            cpf (str): CPF do responsável a ser removido
            
        Returns:
            bool: True se removeu com sucesso, False caso contrário
            
        Raises:
            ValueError: Se o responsável não pode ser removido
        """
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
        """
        Edita os dados de um responsável existente.
        
        Args:
            cpf (str): CPF do responsável a ser editado
            novo_nome (str): Novo nome
            novo_telefone (str): Novo telefone
            novo_setor (str): Novo setor
            
        Returns:
            bool: True se editou com sucesso, False caso contrário
        """
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
        """
        Verifica se um CPF já está cadastrado.
        
        Args:
            cpf (str): CPF a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        try:
            cpf_formatado = self._responsavel_factory._validar_e_formatar_cpf(cpf)
            return self._responsavel_dao.existe_cpf(cpf_formatado)
        except:
            return False
    
    def obter_setores_disponiveis(self) -> List[str]:
        """
        Retorna lista de setores únicos dos responsáveis cadastrados.
        
        Returns:
            List[str]: Lista de setores únicos ordenados
        """
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
        """
        Filtra responsáveis por setor.
        
        Args:
            setor (str): Setor para filtrar
            
        Returns:
            List[Responsavel]: Lista de responsáveis do setor
        """
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
        
    def gerar_relatorio(self, formato: str = "csv", arquivo: str = None) -> str:
        """
        Gera relatório dos responsáveis em formato especificado.
        
        Args:
            formato (str): "csv" ou "pdf"
            arquivo (str): Caminho do arquivo (obrigatório para PDF)
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            responsaveis = self.listar_responsaveis()

            if formato.lower() == "csv":
                return self._gerar_relatorio_csv(responsaveis)
            elif formato.lower() == "pdf":
                if not arquivo:
                    raise ValueError("Caminho do arquivo é obrigatório para PDF")
                return self.gerar_relatorio_pdf_responsaveis(responsaveis, arquivo)
            else:
                raise ValueError("Formatos suportados: 'csv' ou 'pdf'")

        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            raise

    def _gerar_relatorio_csv(self, responsaveis: List[Responsavel]) -> str:
        """
        Gera relatório CSV de responsáveis.
        
        Args:
            responsaveis (List[Responsavel]): Lista de responsáveis
            
        Returns:
            str: Caminho do arquivo gerado
        """
        import csv
        import os
        
        arquivo = "data/relatorio_responsaveis.csv"
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

    def gerar_relatorio_pdf_responsaveis(self, responsaveis: List[Responsavel], arquivo: str) -> str:
        """
        Gera relatório PDF de responsáveis.
        
        Args:
            responsaveis (List[Responsavel]): Lista de responsáveis
            arquivo (str): Caminho do arquivo
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            from fpdf import FPDF
        except ImportError:
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
    


    # def get_responsaveis_com_bombonas(self) -> List[tuple]: # Quero ver com a Claude
    #     """
    #     Retorna lista de responsáveis com a quantidade de bombonas.
        
    #     Returns:
    #         List[tuple]: Lista de tuplas (responsavel, qtd_bombonas)
    #     """
    #     try:
    #         responsaveis = self._responsavel_dao.listar_todos()
    #         resultado = []
            
    #         for responsavel in responsaveis:
    #             bombonas = self._bombona_dao.buscar_por_responsavel(responsavel.get_cpf())
    #             resultado.append((responsavel, len(bombonas)))
            
    #         return resultado
            
    #     except Exception as e:
    #         print(f"Erro ao buscar responsáveis com bombonas: {e}")
    #         return []

    # def get_estatisticas(self) -> dict:
    #     """
    #     Retorna estatísticas simples sobre os responsáveis.
        
    #     Returns:
    #         dict: Dicionário com estatísticas básicas
    #     """
    #     try:
    #         responsaveis = self.listar_responsaveis()
            
    #         # Contagem por setor
    #         responsaveis_por_setor = {}
    #         bombonas_por_setor = {}
    #         responsaveis_sem_bombonas = 0
            
    #         for responsavel in responsaveis:
    #             setor = responsavel.get_setor()
                
    #             # Conta responsáveis por setor
    #             responsaveis_por_setor[setor] = responsaveis_por_setor.get(setor, 0) + 1
                
    #             # Conta bombonas por setor
    #             bombonas = self._bombona_dao.buscar_por_responsavel(responsavel.get_cpf())
    #             if not bombonas:
    #                 responsaveis_sem_bombonas += 1
                
    #             if setor not in bombonas_por_setor:
    #                 bombonas_por_setor[setor] = 0
    #             bombonas_por_setor[setor] += len(bombonas)
            
    #         # Setor com mais responsáveis
    #         setor_mais_responsaveis = max(responsaveis_por_setor.items(), 
    #                                     key=lambda x: x[1])[0] if responsaveis_por_setor else None
            
    #         return {
    #             'total_responsaveis': len(responsaveis),
    #             'total_setores': len(responsaveis_por_setor),
    #             'responsaveis_por_setor': responsaveis_por_setor,
    #             'bombonas_por_setor': bombonas_por_setor,
    #             'responsaveis_sem_bombonas': responsaveis_sem_bombonas,
    #             'setor_com_mais_responsaveis': setor_mais_responsaveis
    #         }
            
    #     except Exception as e:
    #         print(f"Erro ao calcular estatísticas: {e}")
    #         return {
    #             'total_responsaveis': 0,
    #             'total_setores': 0,
    #             'responsaveis_por_setor': {},
    #             'bombonas_por_setor': {},
    #             'responsaveis_sem_bombonas': 0,
    #             'setor_com_mais_responsaveis': None
    #         }