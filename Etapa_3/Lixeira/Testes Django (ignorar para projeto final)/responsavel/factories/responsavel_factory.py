# responsavel/factories/responsavel_factory.py

import re
from typing import Optional
from responsavel.models import Responsavel


class ResponsavelFactory:
    """
    Factory para criação e validação de objetos Responsavel.
    Implementa o padrão Factory Method com validações robustas.
    """
    
    @staticmethod
    def criar_responsavel(cpf: str, nome: str, telefone: str, setor: str) -> Optional[Responsavel]:
        """
        Cria um novo responsável após validar todos os dados.
        
        Args:
            cpf (str): CPF do responsável (pode conter formatação)
            nome (str): Nome completo do responsável
            telefone (str): Telefone (pode conter formatação)
            setor (str): Setor de trabalho
            
        Returns:
            Optional[Responsavel]: Objeto Responsavel válido ou None se inválido
            
        Raises:
            ValueError: Se algum dado for inválido
        """
        # Validar e formatar CPF
        cpf_limpo = ResponsavelFactory._validar_e_formatar_cpf(cpf)
        if not cpf_limpo:
            raise ValueError("CPF inválido")
        
        # Validar nome
        if not ResponsavelFactory._validar_nome(nome):
            raise ValueError("Nome inválido")
        
        # Validar e formatar telefone
        telefone_limpo = ResponsavelFactory._validar_e_formatar_telefone(telefone)
        if not telefone_limpo:
            raise ValueError("Telefone inválido")
        
        # Validar setor
        if not ResponsavelFactory._validar_setor(setor):
            raise ValueError("Setor inválido")
        
        # Criar e retornar o objeto
        return Responsavel(
            cpf=cpf_limpo,
            nome=nome.strip().title(),  # Formatação do nome
            telefone=telefone_limpo,
            setor=setor.strip().title()  # Formatação do setor
        )
    
    @staticmethod
    def _validar_e_formatar_cpf(cpf: str) -> Optional[str]:
        """
        Valida e formata o CPF, removendo caracteres especiais.
        
        Args:
            cpf (str): CPF a ser validado (pode conter formatação)
            
        Returns:
            Optional[str]: CPF limpo (apenas números) se válido, None se inválido
        """
        if not cpf or not isinstance(cpf, str):
            return None
        
        # Remove formatação (pontos, traços, espaços)
        cpf_limpo = re.sub(r'[^0-9]', '', cpf.strip())
        
        # Verifica se tem exatamente 11 dígitos
        if len(cpf_limpo) != 11:
            return None
        
        # Verifica se não são todos números iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            return None
        
        # Validação dos dígitos verificadores
        if not ResponsavelFactory._validar_digitos_cpf(cpf_limpo):
            return None
        
        return cpf_limpo
    
    @staticmethod
    def _validar_digitos_cpf(cpf: str) -> bool:
        """
        Valida os dígitos verificadores do CPF.
        
        Args:
            cpf (str): CPF com 11 dígitos numéricos
            
        Returns:
            bool: True se os dígitos verificadores estão corretos
        """
        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_digito = (soma * 10) % 11
        if primeiro_digito == 10:
            primeiro_digito = 0
        
        if int(cpf[9]) != primeiro_digito:
            return False
        
        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_digito = (soma * 10) % 11
        if segundo_digito == 10:
            segundo_digito = 0
        
        return int(cpf[10]) == segundo_digito
    
    @staticmethod
    def _validar_nome(nome: str) -> bool:
        """
        Valida o nome do responsável.
        
        Args:
            nome (str): Nome a ser validado
            
        Returns:
            bool: True se o nome é válido
        """
        if not nome or not isinstance(nome, str):
            return False
        
        nome_limpo = nome.strip()
        
        # Verifica se não está vazio após limpeza
        if not nome_limpo:
            return False
        
        # Verifica tamanho mínimo e máximo
        if len(nome_limpo) < 2 or len(nome_limpo) > 100:
            return False
        
        # Verifica se contém apenas letras, espaços e acentos
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome_limpo):
            return False
        
        # Verifica se tem pelo menos um nome e um sobrenome
        palavras = nome_limpo.split()
        if len(palavras) < 2:
            return False
        
        return True
    
    @staticmethod
    def _validar_e_formatar_telefone(telefone: str) -> Optional[str]:
        """
        Valida e formata o telefone, removendo caracteres especiais.
        
        Args:
            telefone (str): Telefone a ser validado (pode conter formatação)
            
        Returns:
            Optional[str]: Telefone limpo (apenas números) se válido, None se inválido
        """
        if not telefone or not isinstance(telefone, str):
            return None
        
        # Remove formatação (parênteses, traços, espaços, +55, etc.)
        telefone_limpo = re.sub(r'[^0-9]', '', telefone.strip())
        
        # Remove código do país se presente (55)
        if telefone_limpo.startswith('55') and len(telefone_limpo) >= 12:
            telefone_limpo = telefone_limpo[2:]
        
        # Verifica se tem 10 ou 11 dígitos (celular com 9 na frente ou fixo)
        if len(telefone_limpo) not in [10, 11]:
            return None
        
        # Se tem 11 dígitos, o terceiro deve ser 9 (celular)
        if len(telefone_limpo) == 11 and telefone_limpo[2] != '9':
            return None
        
        # Verifica se o DDD é válido (11 a 99)
        ddd = telefone_limpo[:2]
        if not (11 <= int(ddd) <= 99):
            return None
        
        return telefone_limpo
    
    @staticmethod
    def _validar_setor(setor: str) -> bool:
        """
        Valida o setor do responsável.
        
        Args:
            setor (str): Setor a ser validado
            
        Returns:
            bool: True se o setor é válido
        """
        if not setor or not isinstance(setor, str):
            return False
        
        setor_limpo = setor.strip()
        
        # Verifica se não está vazio após limpeza
        if not setor_limpo:
            return False
        
        # Verifica tamanho mínimo e máximo
        if len(setor_limpo) < 2 or len(setor_limpo) > 50:
            return False
        
        # Verifica se contém apenas letras, números, espaços e alguns caracteres especiais
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-&/]+$', setor_limpo):
            return False
        
        return True