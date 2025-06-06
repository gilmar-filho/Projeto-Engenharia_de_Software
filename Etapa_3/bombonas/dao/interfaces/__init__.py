"""
Interfaces para os DAOs.
Define os contratos para acesso a dados.
"""

from .bombona_dao_interface import BombonaDAOInterface
from .responsavel_dao_interface import ResponsavelDAOInterface

__all__ = ['BombonaDAOInterface', 'ResponsavelDAOInterface']