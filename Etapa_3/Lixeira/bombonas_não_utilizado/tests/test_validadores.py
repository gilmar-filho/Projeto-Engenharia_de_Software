"""
Testes unitários para os validadores
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validadores import (
    ValidadorCPF, ValidadorTelefone, ValidadorTexto, ValidadorNumerico,
    validar_cpf, formatar_cpf, limpar_cpf, validar_telefone, formatar_telefone
)


class TestValidadorCPF(unittest.TestCase):
    """Testes para o ValidadorCPF."""
    
    def test_cpf_valido(self):
        """Testa CPFs válidos."""
        cpfs_validos = [
            "111.444.777-35",
            "52998224725",
            "529.982.247-25",
            "11144477735"
        ]
        
        for cpf in cpfs_validos:
            with self.subTest(cpf=cpf):
                self.assertTrue(ValidadorCPF.validar(cpf), f"CPF {cpf} deveria ser válido")
    
    def test_cpf_invalido(self):
        """Testa CPFs inválidos."""
        cpfs_invalidos = [
            "123.456.789-01",  # Dígitos verificadores incorretos
            "111.111.111-11",  # Todos os dígitos iguais
            "12345678901",     # Dígitos verificadores incorretos
            "123",             # Muito curto
            "",                # Vazio
            None,              # None
            "abc.def.ghi-jk"   # Não numérico
        ]
        
        for cpf in cpfs_invalidos:
            with self.subTest(cpf=cpf):
                self.assertFalse(ValidadorCPF.validar(cpf), f"CPF {cpf} deveria ser inválido")
    
    def test_formatar_cpf(self):
        """Testa formatação de CPF."""
        self.assertEqual(ValidadorCPF.formatar("11144477735"), "111.444.777-35")
        self.assertEqual(ValidadorCPF.formatar("111.444.777-35"), "111.444.777-35")
        self.assertEqual(ValidadorCPF.formatar("123"), "123")  # CPF inválido mantém formato
    
    def test_limpar_cpf(self):
        """Testa limpeza de CPF."""
        self.assertEqual(ValidadorCPF.limpar("111.444.777-35"), "11144477735")
        self.assertEqual(ValidadorCPF.limpar("11144477735"), "11144477735")
        self.assertEqual(ValidadorCPF.limpar(""), "")
        self.assertEqual(ValidadorCPF.limpar(None), "")


class TestValidadorTelefone(unittest.TestCase):
    """Testes para o ValidadorTelefone."""
    
    def test_telefone_valido(self):
        """Testa telefones válidos."""
        telefones_validos = [
            "11987654321",      # 11 dígitos
            "1134567890",       # 10 dígitos
            "(11) 9 8765-4321", # Formatado 11 dígitos
            "(11) 3456-7890"    # Formatado 10 dígitos
        ]
        
        for tel in telefones_validos:
            with self.subTest(telefone=tel):
                self.assertTrue(ValidadorTelefone.validar(tel), f"Telefone {tel} deveria ser válido")
    
    def test_telefone_invalido(self):
        """Testa telefones inválidos."""
        telefones_invalidos = [
            "123456789",        # 9 dígitos
            "123456789012",     # 12 dígitos
            "0987654321",       # DDD inválido (começa com 0)
            "1087654321",       # DDD inválido (10)
            "",                 # Vazio
            None,               # None
            "abc-def-ghij"      # Não numérico
        ]
        
        for tel in telefones_invalidos:
            with self.subTest(telefone=tel):
                self.assertFalse(ValidadorTelefone.validar(tel), f"Telefone {tel} deveria ser inválido")
    
    def test_formatar_telefone(self):
        """Testa formatação de telefone."""
        self.assertEqual(ValidadorTelefone.formatar("11987654321"), "(11) 9 8765-4321")
        self.assertEqual(ValidadorTelefone.formatar("1134567890"), "(11) 3456-7890")
        self.assertEqual(ValidadorTelefone.formatar("123"), "123")  # Telefone inválido mantém formato
    
    def test_limpar_telefone(self):
        """Testa limpeza de telefone."""
        self.assertEqual(ValidadorTelefone.limpar("(11) 9 8765-4321"), "11987654321")
        self.assertEqual(ValidadorTelefone.limpar("11987654321"), "11987654321")
        self.assertEqual(ValidadorTelefone.limpar(""), "")
        self.assertEqual(ValidadorTelefone.limpar(None), "")


class TestValidadorTexto(unittest.TestCase):
    """Testes para o ValidadorTexto."""
    
    def test_nome_valido(self):
        """Testa nomes válidos."""
        nomes_validos = [
            "João Silva",
            "Maria dos Santos",
            "José da Silva-Santos",
            "Ana O'Connor",
            "Francisco de Assis"
        ]
        
        for nome in nomes_validos:
            with self.subTest(nome=nome):
                self.assertTrue(ValidadorTexto.validar_nome(nome), f"Nome '{nome}' deveria ser válido")
    
    def test_nome_invalido(self):
        """Testa nomes inválidos."""
        nomes_invalidos = [
            "João",             # Apenas um nome
            "J",                # Muito curto
            "João123",          # Contém números
            "João@Silva",       # Caracteres especiais
            "",                 # Vazio
            None,               # None
            "a" * 101          # Muito longo
        ]
        
        for nome in nomes_invalidos:
            with self.subTest(nome=nome):
                self.assertFalse(ValidadorTexto.validar_nome(nome), f"Nome '{nome}' deveria ser inválido")
    
    def test_codigo_valido(self):
        """Testa códigos válidos."""
        codigos_validos = [
            "BQ001",
            "LAB-001",
            "QUI123",
            "BIO-LAB-001"
        ]
        
        for codigo in codigos_validos:
            with self.subTest(codigo=codigo):
                self.assertTrue(ValidadorTexto.validar_codigo(codigo), f"Código '{codigo}' deveria ser válido")
    
    def test_codigo_invalido(self):
        """Testa códigos inválidos."""
        codigos_invalidos = [
            "BQ",               # Muito curto
            "BQ@001",           # Caractere especial
            "BQ 001",           # Espaço
            "",                 # Vazio
            None,               # None
            "a" * 21           # Muito longo
        ]
        
        for codigo in codigos_invalidos:
            with self.subTest(codigo=codigo):
                self.assertFalse(ValidadorTexto.validar_codigo(codigo), f"Código '{codigo}' deveria ser inválido")
    
    def test_formatar_nome(self):
        """Testa formatação de nome."""
        self.assertEqual(ValidadorTexto.formatar_nome("joão silva"), "João Silva")
        self.assertEqual(ValidadorTexto.formatar_nome("MARIA DOS SANTOS"), "Maria Dos Santos")
        self.assertEqual(ValidadorTexto.formatar_nome("  ana  costa  "), "Ana Costa")
        self.assertEqual(ValidadorTexto.formatar_nome(""), "")


class TestValidadorNumerico(unittest.TestCase):
    """Testes para o ValidadorNumerico."""
    
    def test_volume_valido(self):
        """Testa volumes válidos."""
        volumes_validos = [
            0.1,      # Mínimo
            25.5,     # Normal
            100.0,    # Normal
            1000.0    # Máximo
        ]
        
        for volume in volumes_validos:
            with self.subTest(volume=volume):
                self.assertTrue(ValidadorNumerico.validar_volume(volume), f"Volume {volume} deveria ser válido")
    
    def test_volume_invalido(self):
        """Testa volumes inválidos."""
        volumes_invalidos = [
            0.05,     # Menor que mínimo
            1001.0,   # Maior que máximo
            -10.0,    # Negativo
            0,        # Zero
            "abc",    # Não numérico
            None      # None
        ]
        
        for volume in volumes_invalidos:
            with self.subTest(volume=volume):
                self.assertFalse(ValidadorNumerico.validar_volume(volume), f"Volume {volume} deveria ser inválido")
    
    def test_formatar_volume(self):
        """Testa formatação de volume."""
        self.assertEqual(ValidadorNumerico.formatar_volume(25.5), "25.50 L")
        self.assertEqual(ValidadorNumerico.formatar_volume(100.0), "100.00 L")
        self.assertEqual(ValidadorNumerico.formatar_volume(25.567, 1), "25.6 L")


class TestFuncoesConveniencia(unittest.TestCase):
    """Testa as funções de conveniência."""
    
    def test_funcoes_cpf(self):
        """Testa funções de conveniência para CPF."""
        cpf_valido = "111.444.777-35"
        
        self.assertTrue(validar_cpf(cpf_valido))
        self.assertEqual(formatar_cpf("11144477735"), "111.444.777-35")
        self.assertEqual(limpar_cpf(cpf_valido), "11144477735")
    
    def test_funcoes_telefone(self):
        """Testa funções de conveniência para telefone."""
        telefone_valido = "(11) 9 8765-4321"
        
        self.assertTrue(validar_telefone(telefone_valido))
        self.assertEqual(formatar_telefone("11987654321"), "(11) 9 8765-4321")


class TestCPFsReaisValidos(unittest.TestCase):
    """Testa com CPFs que sabemos que são válidos."""
    
    def test_cpfs_conhecidos_validos(self):
        """Testa CPFs que são matematicamente válidos."""
        # CPFs gerados com algoritmo correto
        cpfs_validos = [
            "11144477735",  # Usado nos testes
            "52998224725",  # Usado nos testes
            "12345678909",  # CPF válido
            "98765432100",  # CPF válido
            "11111111111"   # Todos iguais - deve ser inválido
        ]
        
        # Os 4 primeiros devem ser válidos
        for i, cpf in enumerate(cpfs_validos[:4]):
            with self.subTest(cpf=cpf):
                self.assertTrue(ValidadorCPF.validar(cpf), f"CPF {cpf} deveria ser válido")
        
        # O último (todos iguais) deve ser inválido
        self.assertFalse(ValidadorCPF.validar(cpfs_validos[4]), "CPF com todos os dígitos iguais deveria ser inválido")
    
    def test_calculo_digito_verificador(self):
        """Testa o cálculo específico dos dígitos verificadores."""
        # Teste manual do CPF 111.444.777-35
        cpf_base = "111444777"
        
        # Primeiro dígito
        soma1 = sum(int(cpf_base[i]) * (10 - i) for i in range(9))
        resto1 = soma1 % 11
        digito1 = 11 - resto1 if resto1 >= 2 else 0
        
        # Segundo dígito
        cpf_com_primeiro = cpf_base + str(digito1)
        soma2 = sum(int(cpf_com_primeiro[i]) * (11 - i) for i in range(10))
        resto2 = soma2 % 11
        digito2 = 11 - resto2 if resto2 >= 2 else 0
        
        cpf_completo = cpf_base + str(digito1) + str(digito2)
        
        # Verifica se o resultado é o CPF esperado
        self.assertEqual(cpf_completo, "11144477735")
        self.assertTrue(ValidadorCPF.validar(cpf_completo))


def executar_testes():
    """Executa todos os testes de validadores."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    executar_testes()