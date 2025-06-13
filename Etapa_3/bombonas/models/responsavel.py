"""
Classe modelo para Responsável por Bombonas de Resíduos Químicos
"""

class Responsavel:
    """
    Classe que representa um responsável por bombonas de resíduos químicos.
    """
    
    def __init__(self, cpf: str, nome: str, telefone: str, setor: str):
        """ Inicializa uma nova instância de Responsavel. """
        self._cpf = cpf
        self._nome = nome
        self._telefone = telefone
        self._setor = setor
    
    # Getters
    def get_cpf(self) -> str:
        """ Retorna o CPF do responsável. """
        return self._cpf
    
    def get_nome(self) -> str:
        """ Retorna o nome do responsável. """
        return self._nome
    
    def get_telefone(self) -> str:
        """ Retorna o telefone do responsável. """
        return self._telefone
    
    def get_setor(self) -> str:
        """ Retorna o setor do responsável. """
        return self._setor
    
    # Setters
    def set_nome(self, novo_nome: str) -> None:
        """ Define um novo nome para o responsável. """
        self._nome = novo_nome
    
    def set_telefone(self, novo_telefone: str) -> None:
        """ Define um novo telefone para o responsável. """
        self._telefone = novo_telefone
    
    def set_setor(self, novo_setor: str) -> None:
        """ Define um novo setor para o responsável. """
        self._setor = novo_setor
    