# responsavel/dao/responsavel_dao_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from responsavel.models import Responsavel


class ResponsavelDAOInterface(ABC):
    """
    Interface para operações de persistência da entidade Responsavel.
    Define os métodos que devem ser implementados por qualquer DAO concreto.
    """
    
    @abstractmethod
    def salvar(self, responsavel: Responsavel) -> None:
        """
        Salva um responsável no banco de dados.
        
        Args:
            responsavel (Responsavel): O responsável a ser salvo
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Responsavel]:
        """
        Lista todos os responsáveis cadastrados.
        
        Returns:
            List[Responsavel]: Lista com todos os responsáveis
        """
        pass
    
    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Responsavel]:
        """
        Busca um responsável pelo seu CPF.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            Optional[Responsavel]: O responsável encontrado ou None
        """
        pass
    
    @abstractmethod
    def remover(self, responsavel: Responsavel) -> None:
        """
        Remove um responsável do banco de dados.
        
        Args:
            responsavel (Responsavel): O responsável a ser removido
        """
        pass
    
    @abstractmethod
    def atualizar(self, responsavel: Responsavel) -> None:
        """
        Atualiza os dados de um responsável existente.
        
        Args:
            responsavel (Responsavel): O responsável com os dados atualizados
        """
        pass
    
    @abstractmethod
    def existe_cpf(self, cpf: str) -> bool:
        """
        Verifica se já existe um responsável com o CPF informado.
        
        Args:
            cpf (str): CPF a ser verificado
            
        Returns:
            bool: True se o CPF já existe, False caso contrário
        """
        pass