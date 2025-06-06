"""
Classe modelo para Bombona de Resíduos Químicos
"""

class Bombona:
    """
    Classe que representa uma bombona de resíduos químicos.
    
    Attributes:
        codigo (str): Código único identificador da bombona
        volume (float): Volume da bombona em litros
        tipo_residuo (str): Tipo de resíduo armazenado
        responsavel: Instância da classe Responsavel
    """
    
    def __init__(self, codigo: str, volume: float, tipo_residuo: str, responsavel):
        """
        Inicializa uma nova instância de Bombona.
        
        Args:
            codigo (str): Código único da bombona
            volume (float): Volume em litros
            tipo_residuo (str): Tipo de resíduo
            responsavel (Responsavel): Responsável pela bombona
        """
        self._codigo = codigo
        self._volume = volume
        self._tipo_residuo = tipo_residuo
        self._responsavel = responsavel
    
    # Getters
    def get_codigo(self) -> str:
        """Retorna o código da bombona."""
        return self._codigo
    
    def get_volume(self) -> float:
        """Retorna o volume da bombona."""
        return self._volume
    
    def get_tipo_residuo(self) -> str:
        """Retorna o tipo de resíduo da bombona."""
        return self._tipo_residuo
    
    def get_responsavel(self):
        """Retorna o responsável pela bombona."""
        return self._responsavel
    
    # Setters
    def set_volume(self, novo_volume: float) -> None:
        """
        Define um novo volume para a bombona.
        
        Args:
            novo_volume (float): Novo volume em litros
        """
        self._volume = novo_volume
    
    def set_tipo_residuo(self, novo_tipo: str) -> None:
        """
        Define um novo tipo de resíduo para a bombona.
        
        Args:
            novo_tipo (str): Novo tipo de resíduo
        """
        self._tipo_residuo = novo_tipo
    
    def set_responsavel(self, novo_responsavel) -> None:
        """
        Define um novo responsável para a bombona.
        
        Args:
            novo_responsavel (Responsavel): Novo responsável
        """
        self._responsavel = novo_responsavel
    
    def __str__(self) -> str:
        """Representação em string da bombona."""
        return f"Bombona[{self._codigo}] - Volume: {self._volume}L - Tipo: {self._tipo_residuo} - Responsável: {self._responsavel.get_nome() if self._responsavel else 'N/A'}"
    
    def __repr__(self) -> str:
        """Representação para debug da bombona."""
        return f"Bombona(codigo='{self._codigo}', volume={self._volume}, tipo_residuo='{self._tipo_residuo}', responsavel={repr(self._responsavel)})"
    
    def __eq__(self, other) -> bool:
        """Compara duas bombonas baseado no código."""
        if not isinstance(other, Bombona):
            return False
        return self._codigo == other._codigo
    
    def __hash__(self) -> int:
        """Hash baseado no código da bombona."""
        return hash(self._codigo)
    
    def to_dict(self) -> dict:
        """
        Converte a bombona para dicionário.
        
        Returns:
            dict: Dicionário com os dados da bombona
        """
        return {
            'codigo': self._codigo,
            'volume': self._volume,
            'tipo_residuo': self._tipo_residuo,
            'cpf_responsavel': self._responsavel.get_cpf() if self._responsavel else None
        }
    
    @classmethod
    def from_dict(cls, data: dict, responsavel=None):
        """
        Cria uma instância de Bombona a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com os dados da bombona
            responsavel (Responsavel): Instância do responsável
            
        Returns:
            Bombona: Nova instância de Bombona
        """
        return cls(
            codigo=data['codigo'],
            volume=float(data['volume']),
            tipo_residuo=data['tipo_residuo'],
            responsavel=responsavel
        )