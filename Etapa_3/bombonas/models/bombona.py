"""
Classe modelo para Bombona de Resíduos Químicos
"""

class Bombona:
    """
    Classe que representa uma bombona de resíduos químicos.
    """
    
    def __init__(self, codigo: str, volume: float, tipo_residuo: str, responsavel):
        """ Inicializa uma nova instância de Bombona. """
        self._codigo = codigo
        self._volume = volume
        self._tipo_residuo = tipo_residuo
        self._responsavel = responsavel
    
    # Getters
    def get_codigo(self) -> str:
        """ Retorna o código da bombona. """
        return self._codigo
    
    def get_volume(self) -> float:
        """ Retorna o volume da bombona. """
        return self._volume
    
    def get_tipo_residuo(self) -> str:
        """ Retorna o tipo de resíduo da bombona. """
        return self._tipo_residuo
    
    def get_responsavel(self):
        """ Retorna o responsável pela bombona. """
        return self._responsavel
    
    # Setters
    def set_volume(self, novo_volume: float) -> None:
        """ Define um novo volume para a bombona. """
        self._volume = novo_volume
    
    def set_tipo_residuo(self, novo_tipo: str) -> None:
        """ Define um novo tipo de resíduo para a bombona. """
        self._tipo_residuo = novo_tipo
    
    def set_responsavel(self, novo_responsavel) -> None:
        """ Define um novo responsável para a bombona. """
        self._responsavel = novo_responsavel