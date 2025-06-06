"""
Utilitário para gerar CPFs válidos para testes
"""

import random


def gerar_cpf_valido() -> str:
    """
    Gera um CPF válido aleatório.
    
    Returns:
        str: CPF válido apenas com números
    """
    # Gera os 9 primeiros dígitos aleatoriamente
    cpf_base = [random.randint(0, 9) for _ in range(9)]
    
    # Calcula o primeiro dígito verificador
    soma = sum(cpf_base[i] * (10 - i) for i in range(9))
    resto = soma % 11
    primeiro_digito = 11 - resto if resto >= 2 else 0
    
    # Adiciona o primeiro dígito
    cpf_base.append(primeiro_digito)
    
    # Calcula o segundo dígito verificador
    soma = sum(cpf_base[i] * (11 - i) for i in range(10))
    resto = soma % 11
    segundo_digito = 11 - resto if resto >= 2 else 0
    
    # Adiciona o segundo dígito
    cpf_base.append(segundo_digito)
    
    # Converte para string
    return ''.join(map(str, cpf_base))


def gerar_cpfs_para_testes(quantidade: int = 5) -> list:
    """
    Gera uma lista de CPFs válidos para usar em testes.
    
    Args:
        quantidade (int): Quantidade de CPFs a gerar
        
    Returns:
        list: Lista de CPFs válidos
    """
    cpfs = []
    for _ in range(quantidade):
        cpf = gerar_cpf_valido()
        # Garante que não são todos os dígitos iguais
        if cpf != cpf[0] * 11:
            cpfs.append(cpf)
    
    return cpfs


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF para exibição.
    
    Args:
        cpf (str): CPF apenas com números
        
    Returns:
        str: CPF formatado
    """
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def main():
    """Função principal para demonstração."""
    print("=== GERADOR DE CPFs VÁLIDOS PARA TESTES ===\n")
    
    # Gera alguns CPFs para demonstração
    cpfs = gerar_cpfs_para_testes(10)
    
    print("CPFs válidos gerados:")
    for i, cpf in enumerate(cpfs, 1):
        cpf_formatado = formatar_cpf(cpf)
        print(f"{i:2d}. {cpf} | {cpf_formatado}")
    
    print("\n=== CPFs FIXOS PARA USAR NOS TESTES ===")
    cpfs_fixos = [
        "11144477735",  # CPF válido fixo 1
        "52998224725",  # CPF válido fixo 2
        "12345678909",  # CPF válido fixo 3
        "98765432100",  # CPF válido fixo 4
        "11122233396"   # CPF válido fixo 5
    ]
    
    print("CPFs fixos recomendados para testes:")
    for i, cpf in enumerate(cpfs_fixos, 1):
        cpf_formatado = formatar_cpf(cpf)
        print(f"{i}. {cpf} | {cpf_formatado}")
    
    # Verifica se todos são válidos
    from validadores import ValidadorCPF
    
    print("\n=== VERIFICAÇÃO DOS CPFs FIXOS ===")
    for cpf in cpfs_fixos:
        valido = ValidadorCPF.validar(cpf)
        status = "✓ VÁLIDO" if valido else "✗ INVÁLIDO"
        print(f"{formatar_cpf(cpf)}: {status}")


if __name__ == "__main__":
    main()