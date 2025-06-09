"""
Classe modelo para Responsável por Bombonas de Resíduos Químicos
"""

class Responsavel:
    """
    Classe que representa um responsável por bombonas de resíduos químicos.
    
    Attributes:
        cpf (str): CPF do responsável
        nome (str): Nome completo do responsável
        telefone (str): Telefone de contato
        setor (str): Setor onde trabalha
    """
    
    def __init__(self, cpf: str, nome: str, telefone: str, setor: str):
        """
        Inicializa uma nova instância de Responsavel.
        
        Args:
            cpf (str): CPF do responsável
            nome (str): Nome completo
            telefone (str): Telefone de contato
            setor (str): Setor de trabalho
        """
        self._cpf = cpf
        self._nome = nome
        self._telefone = telefone
        self._setor = setor
    
    # Getters
    def get_cpf(self) -> str:
        """Retorna o CPF do responsável."""
        return self._cpf
    
    def get_nome(self) -> str:
        """Retorna o nome do responsável."""
        return self._nome
    
    def get_telefone(self) -> str:
        """Retorna o telefone do responsável."""
        return self._telefone
    
    def get_setor(self) -> str:
        """Retorna o setor do responsável."""
        return self._setor
    
    # Setters
    def set_nome(self, novo_nome: str) -> None:
        """
        Define um novo nome para o responsável.
        
        Args:
            novo_nome (str): Novo nome
        """
        self._nome = novo_nome
    
    def set_telefone(self, novo_telefone: str) -> None:
        """
        Define um novo telefone para o responsável.
        
        Args:
            novo_telefone (str): Novo telefone
        """
        self._telefone = novo_telefone
    
    def set_setor(self, novo_setor: str) -> None:
        """
        Define um novo setor para o responsável.
        
        Args:
            novo_setor (str): Novo setor
        """
        self._setor = novo_setor
    
    # def __str__(self) -> str:
    #     """Representação em string do responsável."""
    #     return f"{self._nome} - CPF: {self._cpf} - Setor: {self._setor}"
    
    # def __repr__(self) -> str:
    #     """Representação para debug do responsável."""
    #     return f"Responsavel(cpf='{self._cpf}', nome='{self._nome}', telefone='{self._telefone}', setor='{self._setor}')"
    
    # def __eq__(self, other) -> bool:
    #     """Compara dois responsáveis baseado no CPF."""
    #     if not isinstance(other, Responsavel):
    #         return False
    #     return self._cpf == other._cpf
    
    # def __hash__(self) -> int:
    #     """Hash baseado no CPF do responsável."""
    #     return hash(self._cpf)
    
    # def to_dict(self) -> dict:
    #     """
    #     Converte o responsável para dicionário.
        
    #     Returns:
    #         dict: Dicionário com os dados do responsável
    #     """
    #     return {
    #         'cpf': self._cpf,
    #         'nome': self._nome,
    #         'telefone': self._telefone,
    #         'setor': self._setor
    #     }
    
    # @classmethod
    # def from_dict(cls, data: dict):
    #     """
    #     Cria uma instância de Responsavel a partir de um dicionário.
        
    #     Args:
    #         data (dict): Dicionário com os dados do responsável
            
    #     Returns:
    #         Responsavel: Nova instância de Responsavel
    #     """
    #     return cls(
    #         cpf=data['cpf'],
    #         nome=data['nome'],
    #         telefone=data['telefone'],
    #         setor=data['setor']
    #     )