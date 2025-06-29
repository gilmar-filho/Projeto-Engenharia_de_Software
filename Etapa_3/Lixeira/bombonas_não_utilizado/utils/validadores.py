"""
Módulo de utilitários para validação de dados
"""

import re
from typing import Union


class ValidadorCPF:
    """Classe para validação de CPF."""
    
    @staticmethod
    def validar(cpf: str) -> bool:
        """
        Valida um CPF.
        
        Args:
            cpf (str): CPF a ser validado
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not cpf or not isinstance(cpf, str):
            return False
        
        # Remove caracteres não numéricos
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            return False
        
        # Verifica se não são todos os dígitos iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Validação do dígito verificador
        return ValidadorCPF._validar_digitos(cpf_limpo)
    
    @staticmethod
    def _validar_digitos(cpf: str) -> bool:
        """Valida os dígitos verificadores do CPF."""
        # Primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        primeiro_digito = 11 - resto if resto >= 2 else 0
        
        if int(cpf[9]) != primeiro_digito:
            return False
        
        # Segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        segundo_digito = 11 - resto if resto >= 2 else 0
        
        return int(cpf[10]) == segundo_digito
    
    @staticmethod
    def formatar(cpf: str) -> str:
        """
        Formata um CPF para exibição.
        
        Args:
            cpf (str): CPF apenas com números
            
        Returns:
            str: CPF formatado (XXX.XXX.XXX-XX)
        """
        cpf_limpo = re.sub(r'\D', '', cpf)
        if len(cpf_limpo) == 11:
            return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        return cpf
    
    @staticmethod
    def limpar(cpf: str) -> str:
        """
        Remove formatação do CPF.
        
        Args:
            cpf (str): CPF com ou sem formatação
            
        Returns:
            str: CPF apenas com números
        """
        return re.sub(r'\D', '', cpf) if cpf else ""


class ValidadorTelefone:
    """Classe para validação de telefone."""
    
    @staticmethod
    def validar(telefone: str) -> bool:
        """
        Valida um telefone.
        
        Args:
            telefone (str): Telefone a ser validado
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not telefone or not isinstance(telefone, str):
            return False
        
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        # Aceita telefones com 10 ou 11 dígitos
        if len(telefone_limpo) not in [10, 11]:
            return False
        
        # Verifica DDD válido (11-99)
        if len(telefone_limpo) >= 2:
            ddd = int(telefone_limpo[:2])
            if ddd < 11 or ddd > 99:
                return False
        
        return True
    
    @staticmethod
    def formatar(telefone: str) -> str:
        """
        Formata um telefone para exibição.
        
        Args:
            telefone (str): Telefone apenas com números
            
        Returns:
            str: Telefone formatado
        """
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        if len(telefone_limpo) == 11:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2]} {telefone_limpo[3:7]}-{telefone_limpo[7:]}"
        elif len(telefone_limpo) == 10:
            return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
        
        return telefone
    
    @staticmethod
    def limpar(telefone: str) -> str:
        """
        Remove formatação do telefone.
        
        Args:
            telefone (str): Telefone com ou sem formatação
            
        Returns:
            str: Telefone apenas com números
        """
        return re.sub(r'\D', '', telefone) if telefone else ""


class ValidadorTexto:
    """Classe para validação de texto."""
    
    @staticmethod
    def validar_nome(nome: str, min_length: int = 2, max_length: int = 100) -> bool:
        """
        Valida um nome.
        
        Args:
            nome (str): Nome a ser validado
            min_length (int): Tamanho mínimo
            max_length (int): Tamanho máximo
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not nome or not isinstance(nome, str):
            return False
        
        nome = nome.strip()
        
        if len(nome) < min_length or len(nome) > max_length:
            return False
        
        # Aceita apenas letras, espaços, hífens e apostrofes
        if not re.match(r"^[A-Za-zÀ-ÿ\s\-']+$", nome):
            return False
        
        # Verifica se tem pelo menos duas palavras
        partes = nome.split()
        return len(partes) >= 2
    
    @staticmethod
    def validar_codigo(codigo: str, min_length: int = 3, max_length: int = 20) -> bool:
        """
        Valida um código.
        
        Args:
            codigo (str): Código a ser validado
            min_length (int): Tamanho mínimo
            max_length (int): Tamanho máximo
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not codigo or not isinstance(codigo, str):
            return False
        
        codigo = codigo.strip()
        
        if len(codigo) < min_length or len(codigo) > max_length:
            return False
        
        # Aceita apenas letras, números e hífens
        return bool(re.match(r'^[A-Za-z0-9\-]+$', codigo))
    
    @staticmethod
    def formatar_nome(nome: str) -> str:
        """
        Formata um nome para a forma padrão.
        
        Args:
            nome (str): Nome a ser formatado
            
        Returns:
            str: Nome formatado (Title Case)
        """
        if not nome:
            return ""
        
        return nome.strip().title()


class ValidadorNumerico:
    """Classe para validação de valores numéricos."""
    
    @staticmethod
    def validar_volume(volume: Union[int, float], min_val: float = 0.1, max_val: float = 1000.0) -> bool:
        """
        Valida um volume.
        
        Args:
            volume: Volume a ser validado
            min_val (float): Valor mínimo
            max_val (float): Valor máximo
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not isinstance(volume, (int, float)):
            return False
        
        return min_val <= volume <= max_val
    
    @staticmethod
    def formatar_volume(volume: float, casas_decimais: int = 2) -> str:
        """
        Formata um volume para exibição.
        
        Args:
            volume (float): Volume a ser formatado
            casas_decimais (int): Número de casas decimais
            
        Returns:
            str: Volume formatado
        """
        return f"{volume:.{casas_decimais}f} L"


class ValidadorLista:
    """Classe para validação usando listas de valores válidos."""
    
    @staticmethod
    def validar_item_lista(item: str, lista_valida: list, case_sensitive: bool = False) -> bool:
        """
        Valida se um item está numa lista de valores válidos.
        
        Args:
            item (str): Item a ser validado
            lista_valida (list): Lista de valores válidos
            case_sensitive (bool): Se deve considerar maiúsculas/minúsculas
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not item or not isinstance(item, str):
            return False
        
        if case_sensitive:
            return item in lista_valida
        else:
            return item.upper() in [v.upper() for v in lista_valida]


def validar_entrada_obrigatoria(valor: str, nome_campo: str = "Campo") -> None:
    """
    Valida se uma entrada obrigatória foi preenchida.
    
    Args:
        valor (str): Valor a ser validado
        nome_campo (str): Nome do campo para a mensagem de erro
        
    Raises:
        ValueError: Se o valor estiver vazio
    """
    if not valor or not valor.strip():
        raise ValueError(f"{nome_campo} é obrigatório e não pode estar vazio")


def sanitizar_entrada(texto: str) -> str:
    """
    Sanitiza uma entrada de texto removendo caracteres perigosos.
    
    Args:
        texto (str): Texto a ser sanitizado
        
    Returns:
        str: Texto sanitizado
    """
    if not texto:
        return ""
    
    # Remove caracteres de controle e quebras de linha desnecessárias
    texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto)
    
    # Remove múltiplos espaços
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()


# Funções de conveniência para uso direto
def validar_cpf(cpf: str) -> bool:
    """Função de conveniência para validar CPF."""
    return ValidadorCPF.validar(cpf)


def formatar_cpf(cpf: str) -> str:
    """Função de conveniência para formatar CPF."""
    return ValidadorCPF.formatar(cpf)


def limpar_cpf(cpf: str) -> str:
    """Função de conveniência para limpar CPF."""
    return ValidadorCPF.limpar(cpf)


def validar_telefone(telefone: str) -> bool:
    """Função de conveniência para validar telefone."""
    return ValidadorTelefone.validar(telefone)


def formatar_telefone(telefone: str) -> str:
    """Função de conveniência para formatar telefone."""
    return ValidadorTelefone.formatar(telefone)


def limpar_telefone(telefone: str) -> str:
    """Função de conveniência para limpar telefone."""
    return ValidadorTelefone.limpar(telefone)


def validar_nome(nome: str) -> bool:
    """Função de conveniência para validar nome."""
    return ValidadorTexto.validar_nome(nome)


def validar_codigo(codigo: str) -> bool:
    """Função de conveniência para validar código."""
    return ValidadorTexto.validar_codigo(codigo)


def validar_volume(volume: Union[int, float]) -> bool:
    """Função de conveniência para validar volume."""
    return ValidadorNumerico.validar_volume(volume)


# Teste das validações (para desenvolvimento)
def testar_validadores():
    """Função para testar os validadores durante desenvolvimento."""
    print("=== TESTANDO VALIDADORES ===")
    
    # Teste CPF
    print("\n--- CPF ---")
    cpfs_teste = ["123.456.789-01", "111.111.111-11", "12345678901", "123"]
    for cpf in cpfs_teste:
        valido = validar_cpf(cpf)
        formatado = formatar_cpf(cpf)
        print(f"CPF: {cpf} | Válido: {valido} | Formatado: {formatado}")
    
    # Teste Telefone
    print("\n--- TELEFONE ---")
    telefones_teste = ["11987654321", "(11) 9 8765-4321", "1234567890", "123"]
    for tel in telefones_teste:
        valido = validar_telefone(tel)
        formatado = formatar_telefone(tel)
        print(f"Telefone: {tel} | Válido: {valido} | Formatado: {formatado}")
    
    # Teste Nome
    print("\n--- NOME ---")
    nomes_teste = ["João Silva", "Maria", "José da Silva Santos", "João123"]
    for nome in nomes_teste:
        valido = validar_nome(nome)
        formatado = ValidadorTexto.formatar_nome(nome)
        print(f"Nome: {nome} | Válido: {valido} | Formatado: {formatado}")
    
    # Teste Volume
    print("\n--- VOLUME ---")
    volumes_teste = [25.5, 0.05, 1001, -10, "abc"]
    for vol in volumes_teste:
        try:
            valido = validar_volume(vol)
            formatado = ValidadorNumerico.formatar_volume(vol) if isinstance(vol, (int, float)) else "N/A"
            print(f"Volume: {vol} | Válido: {valido} | Formatado: {formatado}")
        except:
            print(f"Volume: {vol} | Erro na validação")
    
    print("\n=== FIM DOS TESTES ===")


if __name__ == "__main__":
    testar_validadores()