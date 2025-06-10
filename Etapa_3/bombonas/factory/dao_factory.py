"""
Factory para criação de instâncias de DAOs - Versão com baixo acoplamento
"""

from dao.interfaces.responsavel_dao_interface import ResponsavelDAOInterface
from dao.interfaces.bombona_dao_interface import BombonaDAOInterface


class DAOFactory:
    """
    Factory responsável por criar instâncias de DAOs.
    Implementa o padrão Factory Method com baixo acoplamento.
    
    IMPORTANTE: As implementações concretas são importadas dinamicamente
    para manter o baixo acoplamento.
    """
    
    @staticmethod
    def criar_responsavel_dao() -> ResponsavelDAOInterface:
        """
        Cria uma instância do DAO de Responsável.
        
        Returns:
            ResponsavelDAOInterface: Instância do DAO de responsável
        """
        # Import dinâmico para manter baixo acoplamento
        from dao.responsavel_dao import ResponsavelDAO
        return ResponsavelDAO()
    
    @staticmethod
    def criar_bombona_dao() -> BombonaDAOInterface:
        """
        Cria uma instância do DAO de Bombona.
        
        Returns:
            BombonaDAOInterface: Instância do DAO de bombona
        """
        # Import dinâmico para manter baixo acoplamento
        from dao.bombona_dao import BombonaDAO
        return BombonaDAO()
    
    @classmethod
    def criar_todos_daos(cls) -> dict:
        """
        Cria todas as instâncias de DAOs necessárias.
        
        Returns:
            dict: Dicionário com todas as instâncias de DAOs
        """
        return {
            'responsavel_dao': cls.criar_responsavel_dao(),
            'bombona_dao': cls.criar_bombona_dao()
        }