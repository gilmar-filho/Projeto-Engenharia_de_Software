"""
Interface para o DAO de Responsável
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from models.responsavel import Responsavel


class ResponsavelDAOInterface(ABC):
    """
    Interface que define as operações de acesso a dados para Responsavel.
    Esta interface garante baixo acoplamento entre as camadas e define
    o contrato que todas as implementações de DAO de Responsavel devem seguir.
    
    Conforme o diagrama de classes, deve implementar:
    - salvar(r: Responsavel): void
    - listarTodos(): List<Responsavel>
    - buscarPorCPF(cpf: String): Responsavel
    - remover(r: Responsavel): void
    - atualizar(r: Responsavel): void
    - existeCPF(cpf: String): boolean
    """
    
    @abstractmethod
    def salvar(self, responsavel: Responsavel) -> None:
        """ Salva um responsável no repositório de dados. """

        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Responsavel]:
        """ Lista todos os responsáveis do repositório. """

        pass
    
    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Responsavel]:
        """ Busca um responsável pelo CPF. """

        pass
    
    @abstractmethod
    def remover(self, responsavel: Responsavel) -> None:
        """ Remove um responsável do repositório. """

        pass
    
    @abstractmethod
    def atualizar(self, responsavel: Responsavel) -> None:
        """ Atualiza os dados de um responsável existente. """

        pass
    
    @abstractmethod
    def existe_cpf(self, cpf: str) -> bool:
        """ Verifica se existe um responsável com o CPF informado. """
        
        pass