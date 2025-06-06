"""
Módulo de factories.
Implementa o padrão Factory Method para criação de objetos.
"""

from .bombona_factory import BombonaFactory
from .responsavel_factory import ResponsavelFactory

__all__ = ['BombonaFactory', 'ResponsavelFactory']