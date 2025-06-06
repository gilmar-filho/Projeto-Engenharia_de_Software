"""
Factory para criação de instâncias de Responsável com validação
"""

import re
from models.responsavel import Responsavel


class ResponsavelFactory:
    """
    Factory responsável por criar instâncias de Responsavel com validação.
    Implementa o padrão Factory Method para garantir que apenas 
    responsáveis válidos sejam criados.
    """
    
    # Setores sugeridos (para orientação do usuário, mas não limitantes)
    SETORES_SUGERIDOS = [
        'LABORATÓRIO',
        'QUÍMICA',
        'BIOLOGIA', 
        'FÍSICA',
        'ENGENHARIA',
        'MEDICINA',
        'FARMÁCIA',
        'VETERINÁRIA',
        'AGRONOMIA',
        'MANUTENÇÃO',
        'SEGURANÇA',
        'ADMINISTRAÇÃO'
    ]
    
    @classmethod
    def criar_responsavel(cls, cpf: str, nome: str, telefone: str, setor: str) -> Responsavel:
        """
        Cria uma nova instância de Responsavel com validação.
        
        Args:
            cpf (str): CPF do responsável
            nome (str): Nome completo
            telefone (str): Telefone de contato
            setor (str): Setor de trabalho
            
        Returns:
            Responsavel: Nova instância validada de Responsavel
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        # Valida e formata todos os parâmetros
        cpf_formatado = cls._validar_e_formatar_cpf(cpf)
        nome_formatado = cls._validar_e_formatar_nome(nome)
        telefone_formatado = cls._validar_e_formatar_telefone(telefone)
        setor_formatado = cls._validar_e_formatar_setor(setor)
        
        # Cria e retorna o responsável
        return Responsavel(cpf_formatado, nome_formatado, telefone_formatado, setor_formatado)
    
    @classmethod
    def _validar_e_formatar_cpf(cls, cpf: str) -> str:
        """
        Valida e formata o CPF.
        
        Args:
            cpf (str): CPF a ser validado
            
        Returns:
            str: CPF formatado (apenas números)
            
        Raises:
            ValueError: Se o CPF for inválido
        """
        if not cpf or not isinstance(cpf, str):
            raise ValueError("CPF não pode ser vazio")
        
        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        
        # Verifica se não são todos os dígitos iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            raise ValueError("CPF inválido - todos os dígitos são iguais")
        
        # Validação do dígito verificador
        if not cls._validar_digitos_cpf(cpf_limpo):
            raise ValueError("CPF inválido - dígitos verificadores incorretos")
        
        return cpf_limpo
    
    @classmethod
    def _validar_digitos_cpf(cls, cpf: str) -> bool:
        """
        Valida os dígitos verificadores do CPF.
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            bool: True se os dígitos verificadores estão corretos
        """
        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        primeiro_digito = 11 - resto if resto >= 2 else 0
        
        if int(cpf[9]) != primeiro_digito:
            return False
        
        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        segundo_digito = 11 - resto if resto >= 2 else 0
        
        return int(cpf[10]) == segundo_digito
    
    @classmethod
    def _validar_e_formatar_nome(cls, nome: str) -> str:
        """
        Valida e formata o nome do responsável.
        
        Args:
            nome (str): Nome a ser validado
            
        Returns:
            str: Nome formatado (Title Case)
            
        Raises:
            ValueError: Se o nome for inválido
        """
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome não pode ser vazio")
        
        nome = nome.strip()
        
        if len(nome) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        
        if len(nome) > 100:
            raise ValueError("Nome não pode exceder 100 caracteres")
        
        # Aceita apenas letras, espaços, hífens e apostrofes
        if not re.match(r"^[A-Za-zÀ-ÿ\s\-']+$", nome):
            raise ValueError("Nome deve conter apenas letras, espaços, hífens e apostrofes")
        
        # Verifica se tem pelo menos um nome e um sobrenome
        partes_nome = nome.split()
        if len(partes_nome) < 2:
            raise ValueError("Nome completo deve conter pelo menos nome e sobrenome")
        
        # Formata em Title Case
        return nome.title()
    
    @classmethod
    def _validar_e_formatar_telefone(cls, telefone: str) -> str:
        """
        Valida e formata o telefone.
        
        Args:
            telefone (str): Telefone a ser validado
            
        Returns:
            str: Telefone formatado (apenas números)
            
        Raises:
            ValueError: Se o telefone for inválido
        """
        if not telefone or not isinstance(telefone, str):
            raise ValueError("Telefone não pode ser vazio")
        
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        # Aceita telefones com 10 ou 11 dígitos (com ou sem 9º dígito)
        if len(telefone_limpo) not in [10, 11]:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        
        # Verifica se começa com DDD válido (11-99)
        if len(telefone_limpo) >= 2:
            ddd = int(telefone_limpo[:2])
            if ddd < 11 or ddd > 99:
                raise ValueError("DDD do telefone deve estar entre 11 e 99")
        
        return telefone_limpo
    
    @classmethod
    def _validar_e_formatar_setor(cls, setor: str) -> str:
        """
        Valida e formata o setor.
        O usuário tem liberdade para inserir qualquer setor.
        
        Args:
            setor (str): Setor a ser validado
            
        Returns:
            str: Setor formatado (maiúsculas)
            
        Raises:
            ValueError: Se o setor for inválido
        """
        if not setor or not isinstance(setor, str):
            raise ValueError("Setor não pode ser vazio")
        
        setor = setor.strip()
        
        if len(setor) < 2:
            raise ValueError("Setor deve ter pelo menos 2 caracteres")
        
        if len(setor) > 50:
            raise ValueError("Setor não pode exceder 50 caracteres")
        
        # Aceita letras, números, espaços e alguns caracteres especiais
        if not re.match(r"^[A-Za-zÀ-ÿ0-9\s\-&/]+$", setor):
            raise ValueError("Setor deve conter apenas letras, números, espaços, hífens, & e /")
        
        # Retorna em maiúsculas para padronização
        return setor.upper()
    
    @classmethod
    def get_setores_sugeridos(cls) -> list:
        """
        Retorna a lista de setores sugeridos (não limitantes).
        
        Returns:
            list: Lista de setores sugeridos
        """
        return cls.SETORES_SUGERIDOS.copy()
    
    @classmethod
    def get_setores_validos(cls) -> list:
        """
        Mantém compatibilidade com código existente.
        Retorna setores sugeridos já que agora qualquer setor é válido.
        
        Returns:
            list: Lista de setores sugeridos
        """
        return cls.get_setores_sugeridos()
    
    @classmethod
    def formatar_cpf_para_exibicao(cls, cpf: str) -> str:
        """
        Formata o CPF para exibição (XXX.XXX.XXX-XX).
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            str: CPF formatado para exibição
        """
        if not cpf or len(cpf) != 11:
            return cpf
        
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    @classmethod
    def formatar_telefone_para_exibicao(cls, telefone: str) -> str:
        """
        Formata o telefone para exibição.
        
        Args:
            telefone (str): Telefone apenas com números
            
        Returns:
            str: Telefone formatado para exibição
        """
        if not telefone:
            return telefone
        
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        if len(telefone_limpo) == 11:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2]} {telefone_limpo[3:7]}-{telefone_limpo[7:]}"
        elif len(telefone_limpo) == 10:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone