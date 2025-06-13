"""
Interface para o DAO de Bombona
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from models.bombona import Bombona


class BombonaDAOInterface(ABC):
    """
    Interface que define as operações de acesso a dados para Bombona.
    Esta interface garante baixo acoplamento entre as camadas e define
    o contrato que todas as implementações de DAO de Bombona devem seguir.
    
    Conforme o diagrama de classes, deve implementar:
    - salvar(b: Bombona): void
    - listarTodas(): List<Bombona>
    - buscarPorCodigo(codigo: String): Bombona
    - buscarPorResponsavel(cpf: String): List<Bombona>
    - remover(b: Bombona): void
    - atualizar(b: Bombona): void
    - existeCodigo(codigo: String): boolean
    """
    
    @abstractmethod
    def salvar(self, bombona: Bombona) -> None:
        """ Salva uma bombona no repositório de dados. """

        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Bombona]:
        """ Lista todas as bombonas do repositório. """

        pass
    
    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Bombona]:
        """ Busca uma bombona pelo código. """

        pass
    
    @abstractmethod
    def buscar_por_responsavel(self, cpf: str) -> List[Bombona]:
        """ Busca todas as bombonas de um responsável específico. """

        pass
    
    @abstractmethod
    def remover(self, bombona: Bombona) -> None:
        """ Remove uma bombona do repositório. """

        pass
    
    @abstractmethod
    def atualizar(self, bombona: Bombona) -> None:
        """ Atualiza os dados de uma bombona existente. """

        pass
    
    @abstractmethod
    def existe_codigo(self, codigo: str) -> bool:
        """ Verifica se existe uma bombona com o código informado. """
        
        pass