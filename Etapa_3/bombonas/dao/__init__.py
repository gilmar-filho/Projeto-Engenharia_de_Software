"""
Módulo de acesso a dados (DAO).
Contém as implementações e interfaces para persistência de dados.
"""

from .bombona_dao import BombonaDAO
from .responsavel_dao import ResponsavelDAO

__all__ = ['BombonaDAO', 'ResponsavelDAO']