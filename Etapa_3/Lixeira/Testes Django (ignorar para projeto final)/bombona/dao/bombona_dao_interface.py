# bombona/dao/bombona_dao_interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from bombona.models import Bombona


class BombonaDAOInterface(ABC):
    """
    Interface para operações de persistência da entidade Bombona.
    Define os métodos que devem ser implementados por qualquer DAO concreto.
    """
    
    @abstractmethod
    def salvar(self, bombona: Bombona) -> None:
        """
        Salva uma bombona no banco de dados.
        
        Args:
            bombona (Bombona): A bombona a ser salva
        """
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Bombona]:
        """
        Lista todas as bombonas cadastradas.
        
        Returns:
            List[Bombona]: Lista com todas as bombonas
        """
        pass
    
    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Bombona]:
        """
        Busca uma bombona pelo seu código.
        
        Args:
            codigo (str): Código da bombona
            
        Returns:
            Optional[Bombona]: A bombona encontrada ou None
        """
        pass
    
    @abstractmethod
    def buscar_por_responsavel(self, cpf: str) -> List[Bombona]:
        """
        Busca todas as bombonas de um responsável específico.
        
        Args:
            cpf (str): CPF do responsável
            
        Returns:
            List[Bombona]: Lista das bombonas do responsável
        """
        pass
    
    @abstractmethod
    def remover(self, bombona: Bombona) -> None:
        """
        Remove uma bombona do banco de dados.
        
        Args:
            bombona (Bombona): A bombona a ser removida
        """
        pass
    
    @abstractmethod
    def atualizar(self, bombona: Bombona) -> None:
        """
        Atualiza os dados de uma bombona existente.
        
        Args:
            bombona (Bombona): A bombona com os dados atualizados
        """
        pass
    
    @abstractmethod
    def existe_codigo(self, codigo: str) -> bool:
        """
        Verifica se já existe uma bombona com o código informado.
        
        Args:
            codigo (str): Código a ser verificado
            
        Returns:
            bool: True se o código já existe, False caso contrário
        """
        pass