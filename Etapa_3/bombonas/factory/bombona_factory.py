"""
Factory para criação de instâncias de Bombona com validação
"""

from models.bombona import Bombona

class BombonaFactory:
    """
    Factory responsável por criar instâncias de Bombona com validação.
    Implementa o padrão Factory Method para garantir que apenas 
    bombonas válidas sejam criadas.
    """
    
    # Tipos de resíduos válidos
    TIPOS_RESIDUOS_VALIDOS = [
        'QUÍMICO',
        'BIOLÓGICO'
    ]
    
    @classmethod
    def criar_bombona(cls, codigo: str, volume: float, tipo_residuo: str) -> Bombona:
        """ Cria uma nova instância de Bombona com validação dos dados próprios. """

        # Valida e formata apenas os dados da bombona
        codigo_formatado = cls._validar_e_formatar_codigo(codigo)
        volume_validado = cls._validar_volume(volume)
        tipo_residuo_formatado = cls._validar_e_formatar_tipo_residuo(tipo_residuo)
        
        # Cria e retorna a bombona SEM responsável (será definido pelo Controller)
        return Bombona(codigo_formatado, volume_validado, tipo_residuo_formatado, responsavel=None)
    
    @classmethod
    def _validar_e_formatar_codigo(cls, codigo: str) -> str:
        """
        Valida e formata o código da bombona no formato 'LLL-111' (3 letras + 3 números).
        O usuário pode digitar sem o hífen e em qualquer case.
        """

        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código da bombona não pode ser vazio")
        
        # Remove espaços e converte para maiúsculas
        codigo = codigo.strip().upper()
        
        # Remove hífen se existir (para facilitar a validação)
        codigo_limpo = codigo.replace('-', '')
        
        # Verifica se tem exatamente 6 caracteres
        if len(codigo_limpo) != 6:
            raise ValueError("Código da bombona deve ter exatamente 6 caracteres (3 letras + 3 números)")
        
        # Verifica se os primeiros 3 são letras
        if not codigo_limpo[:3].isalpha():
            raise ValueError("Código da bombona deve começar com 3 letras")
        
        # Verifica se os últimos 3 são números
        if not codigo_limpo[3:].isdigit():
            raise ValueError("Código da bombona deve terminar com 3 números")
        
        # Formata no padrão correto: LLL-111
        codigo_formatado = f"{codigo_limpo[:3]}-{codigo_limpo[3:]}"
        
        return codigo_formatado
    
    @classmethod
    def _validar_volume(cls, volume: float) -> float:
        """ Valida o volume da bombona. """

        if not isinstance(volume, (int, float)):
            try:
                volume = float(volume)
            except (ValueError, TypeError):
                raise ValueError("Volume deve ser um número válido")
        
        if volume <= 0:
            raise ValueError("Volume deve ser maior que zero")
        
        if volume > 10000:  # Limite máximo de 10.000 litros
            raise ValueError("Volume não pode exceder 10.000 litros")
        
        # Limita a 2 casas decimais
        return round(float(volume), 2)
    
    @classmethod
    def _validar_e_formatar_tipo_residuo(cls, tipo_residuo: str) -> str:
        """ Valida e formata o tipo de resíduo. """

        if not tipo_residuo or not isinstance(tipo_residuo, str):
            raise ValueError("Tipo de resíduo não pode ser vazio")
        
        tipo_residuo = tipo_residuo.strip().upper()
        
        if tipo_residuo not in cls.TIPOS_RESIDUOS_VALIDOS:
            tipos_validos = ', '.join(cls.TIPOS_RESIDUOS_VALIDOS)
            raise ValueError(f"Tipo de resíduo inválido. Tipos válidos: {tipos_validos}")
        
        return tipo_residuo
    
    @classmethod
    def get_tipos_residuos_validos(cls) -> list:
        """ Retorna a lista de tipos de resíduos válidos. """

        return cls.TIPOS_RESIDUOS_VALIDOS.copy()