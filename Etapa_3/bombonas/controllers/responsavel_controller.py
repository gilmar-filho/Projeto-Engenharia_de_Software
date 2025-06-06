"""
Controller para gerenciamento de Responsáveis
"""

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
    
    def get_setores_validos(self) -> List[str]:
        """
        Retorna os setores válidos.
        
        Returns:
            List[str]: Lista de setores válidos
        """
        return self._responsavel_factory.get_setores_validos()
    
    def formatar_cpf_para_exibicao(self, cpf: str) -> str:
        """
        Formata o CPF para exibição.
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            str: CPF formatado (XXX.XXX.XXX-XX)
        """
        return self._responsavel_factory.formatar_cpf_para_exibicao(cpf)
    
    def formatar_telefone_para_exibicao(self, telefone: str) -> str:
        """
        Formata o telefone para exibição.
        
        Args:
            telefone (str): Telefone apenas com números
            
        Returns:
            str: Telefone formatado
        """
        return self._responsavel_factory.formatar_telefone_para_exibicao(telefone)
    
    def get_responsaveis_com_bombonas(self) -> List[tuple]:
        """
        Retorna lista de responsáveis com a quantidade de bombonas.
        
        Returns:
            List[tuple]: Lista de tuplas (responsavel, qtd_bombonas)
        """
        try:
            responsaveis = self._responsavel_dao.listar_todos()
            resultado = []
            
            for responsavel in responsaveis:
                bombonas = self._bombona_dao.buscar_por_responsavel(responsavel.get_cpf())
                resultado.append((responsavel, len(bombonas)))
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao buscar responsáveis com bombonas: {e}")
            return []
    
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
    
    def get_estatisticas(self) -> dict:
        """
        Retorna estatísticas sobre os responsáveis.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        try:
            responsaveis = self._responsavel_dao.listar_todos()
            
            # Contagem por setor
            setores = {}
            total_bombonas_por_setor = {}
            
            for responsavel in responsaveis:
                setor = responsavel.get_setor()
                setores[setor] = setores.get(setor, 0) + 1
                
                # Conta bombonas por setor
                bombonas = self._bombona_dao.buscar_por_responsavel(responsavel.get_cpf())
                total_bombonas_por_setor[setor] = total_bombonas_por_setor.get(setor, 0) + len(bombonas)
            
            return {
                'total_responsaveis': len(responsaveis),
                'responsaveis_por_setor': setores,
                'bombonas_por_setor': total_bombonas_por_setor
            }
            
        except Exception as e:
            print(f"Erro ao calcular estatísticas: {e}")
            return {
                'total_responsaveis': 0,
                'responsaveis_por_setor': {},
                'bombonas_por_setor': {}
            }