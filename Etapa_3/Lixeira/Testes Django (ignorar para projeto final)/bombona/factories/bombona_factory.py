# bombona/factories/bombona_factory.py

import re
from typing import Optional
from bombona.models import Bombona
from responsavel.models import Responsavel


class BombonaFactory:
    """
    Factory para criação e validação de objetos Bombona.
    Implementa o padrão Factory Method com validações robustas.
    """
    
    @staticmethod
    def criar_bombona(codigo: str, volume: float, tipo_residuo: str, responsavel: Responsavel) -> Optional[Bombona]:
        """
        Cria uma nova bombona após validar todos os dados.
        
        Args:
            codigo (str): Código único da bombona
            volume (float): Volume da bombona em litros
            tipo_residuo (str): Tipo de resíduo químico
            responsavel (Responsavel): Responsável pela bombona
            
        Returns:
            Optional[Bombona]: Objeto Bombona válido ou None se inválido
            
        Raises:
            ValueError: Se algum dado for inválido
        """
        # Validar código
        if not BombonaFactory._validar_codigo(codigo):
            raise ValueError("Código inválido")
        
        # Validar volume
        if not BombonaFactory._validar_volume(volume):
            raise ValueError("Volume inválido")
        
        # Validar tipo de resíduo
        if not BombonaFactory._validar_tipo_residuo(tipo_residuo):
            raise ValueError("Tipo de resíduo inválido")
        
        # Validar responsável
        if not responsavel or not isinstance(responsavel, Responsavel):
            raise ValueError("Responsável inválido")
        
        # Criar e retornar o objeto
        return Bombona(
            codigo=codigo.strip().upper(),  # Padronização do código
            volume=volume,
            tipo_residuo=tipo_residuo.strip().title(),  # Formatação do tipo
            responsavel=responsavel
        )
    
    @staticmethod
    def _validar_codigo(codigo: str) -> bool:
        """
        Valida o código da bombona.
        
        Args:
            codigo (str): Código a ser validado
            
        Returns:
            bool: True se o código é válido
        """
        if not codigo or not isinstance(codigo, str):
            return False
        
        codigo_limpo = codigo.strip().upper()
        
        # Verifica se não está vazio após limpeza
        if not codigo_limpo:
            return False
        
        # Verifica tamanho (1 a 20 caracteres conforme diagrama)
        if len(codigo_limpo) < 1 or len(codigo_limpo) > 20:
            return False
        
        # Verifica formato: deve conter apenas letras e números
        # Exemplo: D1423, AB123, XYZ789, etc.
        if not re.match(r'^[A-Z0-9]+$', codigo_limpo):
            return False
        
        # Deve ter pelo menos um caractere alfabético
        if not re.search(r'[A-Z]', codigo_limpo):
            return False
        
        # Deve ter pelo menos um número
        if not re.search(r'[0-9]', codigo_limpo):
            return False
        
        return True
    
    @staticmethod
    def _validar_volume(volume) -> bool:
        """
        Valida o volume da bombona.
        
        Args:
            volume: Volume a ser validado
            
        Returns:
            bool: True se o volume é válido
        """
        # Verifica se é um número
        try:
            volume_float = float(volume)
        except (ValueError, TypeError):
            return False
        
        # Verifica se é positivo
        if volume_float <= 0:
            return False
        
        # Verifica limites práticos (0.1L a 1000L)
        if volume_float < 0.1 or volume_float > 1000.0:
            return False
        
        # Verifica se não tem mais de 2 casas decimais
        if round(volume_float, 2) != volume_float:
            return False
        
        return True
    
    @staticmethod
    def _validar_tipo_residuo(tipo_residuo: str) -> bool:
        """
        Valida o tipo de resíduo químico.
        
        Args:
            tipo_residuo (str): Tipo de resíduo a ser validado
            
        Returns:
            bool: True se o tipo de resíduo é válido
        """
        if not tipo_residuo or not isinstance(tipo_residuo, str):
            return False
        
        tipo_limpo = tipo_residuo.strip()
        
        # Verifica se não está vazio após limpeza
        if not tipo_limpo:
            return False
        
        # Verifica tamanho mínimo e máximo
        if len(tipo_limpo) < 2 or len(tipo_limpo) > 100:
            return False
        
        # Verifica se contém apenas caracteres válidos
        # Permite letras, números, espaços, hífens, parênteses e alguns símbolos químicos
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-().,/&%+]+$', tipo_limpo):
            return False
        
        # Lista de tipos de resíduos químicos comuns (validação adicional)
        tipos_validos = [
            'ácido', 'base', 'solvente', 'óleo', 'tinta', 'verniz',
            'reagente', 'corrosivo', 'inflamável', 'tóxico',
            'laboratório', 'industrial', 'hospitalar', 'farmacêutico',
            'pesticida', 'herbicida', 'fertilizante', 'bateria',
            'pilha', 'eletrônico', 'metálico', 'orgânico', 'inorgânico'
        ]
        
        # Verifica se contém pelo menos uma palavra-chave válida (case insensitive)
        tipo_lower = tipo_limpo.lower()
        tem_palavra_valida = any(palavra in tipo_lower for palavra in tipos_validos)
        
        return tem_palavra_valida
    
    @staticmethod
    def validar_dados_bombona(codigo: str, volume, tipo_residuo: str, responsavel) -> dict:
        """
        Valida todos os dados da bombona e retorna um relatório detalhado.
        
        Args:
            codigo (str): Código da bombona
            volume: Volume da bombona
            tipo_residuo (str): Tipo de resíduo
            responsavel: Responsável pela bombona
            
        Returns:
            dict: Relatório de validação com erros específicos
        """
        erros = []
        
        if not BombonaFactory._validar_codigo(codigo):
            erros.append("Código inválido: deve conter letras e números (ex: D1423)")
        
        if not BombonaFactory._validar_volume(volume):
            erros.append("Volume inválido: deve ser um número positivo entre 0.1 e 1000 litros")
        
        if not BombonaFactory._validar_tipo_residuo(tipo_residuo):
            erros.append("Tipo de resíduo inválido: deve ser um tipo químico reconhecido")
        
        if not responsavel or not isinstance(responsavel, Responsavel):
            erros.append("Responsável inválido: deve ser um objeto Responsavel válido")
        
        return {
            'valido': len(erros) == 0,
            'erros': erros
        }