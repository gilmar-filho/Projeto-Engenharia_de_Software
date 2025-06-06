"""
Testes unitários para as classes Model
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.responsavel import Responsavel
from models.bombona import Bombona
from factory.responsavel_factory import ResponsavelFactory
from factory.bombona_factory import BombonaFactory


class TestResponsavel(unittest.TestCase):
    """Testes para a classe Responsavel."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.responsavel = Responsavel(
            cpf="11144477735",  # CPF válido
            nome="João Silva",
            telefone="11987654321",
            setor="LABORATÓRIO"
        )
    
    def test_criacao_responsavel(self):
        """Testa a criação de um responsável."""
        self.assertEqual(self.responsavel.get_cpf(), "11144477735")
        self.assertEqual(self.responsavel.get_nome(), "João Silva")
        self.assertEqual(self.responsavel.get_telefone(), "11987654321")
        self.assertEqual(self.responsavel.get_setor(), "LABORATÓRIO")
    
    def test_setters_responsavel(self):
        """Testa os métodos setters."""
        self.responsavel.set_nome("Maria Santos")
        self.responsavel.set_telefone("11999888777")
        self.responsavel.set_setor("QUÍMICA")
        
        self.assertEqual(self.responsavel.get_nome(), "Maria Santos")
        self.assertEqual(self.responsavel.get_telefone(), "11999888777")
        self.assertEqual(self.responsavel.get_setor(), "QUÍMICA")
    
    def test_to_dict(self):
        """Testa a conversão para dicionário."""
        dados = self.responsavel.to_dict()
        
        self.assertEqual(dados['cpf'], "11144477735")
        self.assertEqual(dados['nome'], "João Silva")
        self.assertEqual(dados['telefone'], "11987654321")
        self.assertEqual(dados['setor'], "LABORATÓRIO")
    
    def test_from_dict(self):
        """Testa a criação a partir de dicionário."""
        dados = {
            'cpf': "52998224725",  # CPF válido
            'nome': "Ana Costa",
            'telefone': "11888777666",
            'setor': "BIOLOGIA"
        }
        
        responsavel = Responsavel.from_dict(dados)
        
        self.assertEqual(responsavel.get_cpf(), "52998224725")
        self.assertEqual(responsavel.get_nome(), "Ana Costa")
        self.assertEqual(responsavel.get_telefone(), "11888777666")
        self.assertEqual(responsavel.get_setor(), "BIOLOGIA")
    
    def test_igualdade_responsavel(self):
        """Testa a comparação entre responsáveis."""
        responsavel2 = Responsavel("11144477735", "Outro Nome", "11111111111", "OUTROS")  # Mesmo CPF
        responsavel3 = Responsavel("52998224725", "João Silva", "11987654321", "LABORATÓRIO")  # CPF diferente
        
        # Mesmo CPF deve ser igual
        self.assertEqual(self.responsavel, responsavel2)
        # CPF diferente deve ser diferente
        self.assertNotEqual(self.responsavel, responsavel3)


class TestBombona(unittest.TestCase):
    """Testes para a classe Bombona."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.responsavel = Responsavel(
            cpf="11144477735",  # CPF válido
            nome="João Silva",
            telefone="11987654321",
            setor="LABORATÓRIO"
        )
        
        self.bombona = Bombona(
            codigo="BQ001",
            volume=50.5,
            tipo_residuo="ÁCIDO",
            responsavel=self.responsavel
        )
    
    def test_criacao_bombona(self):
        """Testa a criação de uma bombona."""
        self.assertEqual(self.bombona.get_codigo(), "BQ001")
        self.assertEqual(self.bombona.get_volume(), 50.5)
        self.assertEqual(self.bombona.get_tipo_residuo(), "ÁCIDO")
        self.assertEqual(self.bombona.get_responsavel(), self.responsavel)
    
    def test_setters_bombona(self):
        """Testa os métodos setters."""
        novo_responsavel = Responsavel("52998224725", "Maria Santos", "11999888777", "QUÍMICA")  # CPF válido
        
        self.bombona.set_volume(75.0)
        self.bombona.set_tipo_residuo("BASE")
        self.bombona.set_responsavel(novo_responsavel)
        
        self.assertEqual(self.bombona.get_volume(), 75.0)
        self.assertEqual(self.bombona.get_tipo_residuo(), "BASE")
        self.assertEqual(self.bombona.get_responsavel(), novo_responsavel)
    
    def test_to_dict(self):
        """Testa a conversão para dicionário."""
        dados = self.bombona.to_dict()
        
        self.assertEqual(dados['codigo'], "BQ001")
        self.assertEqual(dados['volume'], 50.5)
        self.assertEqual(dados['tipo_residuo'], "ÁCIDO")
        self.assertEqual(dados['cpf_responsavel'], "11144477735")
    
    def test_from_dict(self):
        """Testa a criação a partir de dicionário."""
        dados = {
            'codigo': "BQ002",
            'volume': "25.5",
            'tipo_residuo': "SOLVENTE"
        }
        
        bombona = Bombona.from_dict(dados, self.responsavel)
        
        self.assertEqual(bombona.get_codigo(), "BQ002")
        self.assertEqual(bombona.get_volume(), 25.5)
        self.assertEqual(bombona.get_tipo_residuo(), "SOLVENTE")
        self.assertEqual(bombona.get_responsavel(), self.responsavel)
    
    def test_igualdade_bombona(self):
        """Testa a comparação entre bombonas."""
        bombona2 = Bombona("BQ001", 100.0, "BASE", self.responsavel)
        bombona3 = Bombona("BQ002", 50.5, "ÁCIDO", self.responsavel)
        
        # Mesmo código deve ser igual
        self.assertEqual(self.bombona, bombona2)
        # Código diferente deve ser diferente
        self.assertNotEqual(self.bombona, bombona3)


class TestResponsavelFactory(unittest.TestCase):
    """Testes para a ResponsavelFactory."""
    
    def test_criar_responsavel_valido(self):
        """Testa a criação de responsável válido."""
        responsavel = ResponsavelFactory.criar_responsavel(
            cpf="111.444.777-35",  # CPF válido com formatação
            nome="joão da silva",  # Nome em minúsculas para testar formatação
            telefone="(11) 9 8765-4321",  # Telefone formatado
            setor="laboratório"  # Setor em minúsculas
        )
        
        # Verifica se os dados foram processados corretamente
        self.assertEqual(responsavel.get_cpf(), "11144477735")  # CPF limpo
        self.assertEqual(responsavel.get_nome(), "João Da Silva")  # Nome formatado
        self.assertEqual(responsavel.get_telefone(), "11987654321")  # Telefone limpo
        self.assertEqual(responsavel.get_setor(), "LABORATÓRIO")  # Setor em maiúsculas
    
    def test_cpf_invalido(self):
        """Testa validação de CPF inválido."""
        with self.assertRaises(ValueError):
            ResponsavelFactory.criar_responsavel(
                cpf="123.456.789-00",  # CPF inválido
                nome="João Silva",
                telefone="11987654321",
                setor="LABORATÓRIO"
            )
    
    def test_nome_invalido(self):
        """Testa validação de nome inválido."""
        with self.assertRaises(ValueError):
            ResponsavelFactory.criar_responsavel(
                cpf="111.444.777-35",  # CPF válido
                nome="João",  # Apenas um nome
                telefone="11987654321",
                setor="LABORATÓRIO"
            )
    
    def test_setor_invalido(self):
        """Testa validação de setor inválido."""
        with self.assertRaises(ValueError):
            ResponsavelFactory.criar_responsavel(
                cpf="111.444.777-35",  # CPF válido
                nome="João Silva",
                telefone="11987654321",
                setor="SETOR_INEXISTENTE"
            )
    
    def test_telefone_invalido(self):
        """Testa validação de telefone inválido."""
        with self.assertRaises(ValueError):
            ResponsavelFactory.criar_responsavel(
                cpf="111.444.777-35",  # CPF válido
                nome="João Silva",
                telefone="123456789",  # Telefone com poucos dígitos
                setor="LABORATÓRIO"
            )


class TestBombonaFactory(unittest.TestCase):
    """Testes para a BombonaFactory."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.responsavel = Responsavel(
            cpf="11144477735",  # CPF válido
            nome="João Silva",
            telefone="11987654321",
            setor="LABORATÓRIO"
        )
    
    def test_criar_bombona_valida(self):
        """Testa a criação de bombona válida."""
        bombona = BombonaFactory.criar_bombona(
            codigo="BQ-001",
            volume=50.5,
            tipo_residuo="ácido",
            responsavel=self.responsavel
        )
        
        self.assertEqual(bombona.get_codigo(), "BQ-001")
        self.assertEqual(bombona.get_volume(), 50.5)
        self.assertEqual(bombona.get_tipo_residuo(), "ÁCIDO")
        self.assertEqual(bombona.get_responsavel(), self.responsavel)
    
    def test_codigo_invalido(self):
        """Testa validação de código inválido."""
        with self.assertRaises(ValueError):
            BombonaFactory.criar_bombona(
                codigo="BQ",  # Muito curto
                volume=50.5,
                tipo_residuo="ÁCIDO",
                responsavel=self.responsavel
            )
    
    def test_volume_invalido(self):
        """Testa validação de volume inválido."""
        with self.assertRaises(ValueError):
            BombonaFactory.criar_bombona(
                codigo="BQ001",
                volume=-10.0,  # Volume negativo
                tipo_residuo="ÁCIDO",
                responsavel=self.responsavel
            )
    
    def test_tipo_residuo_invalido(self):
        """Testa validação de tipo de resíduo inválido."""
        with self.assertRaises(ValueError):
            BombonaFactory.criar_bombona(
                codigo="BQ001",
                volume=50.5,
                tipo_residuo="TIPO_INEXISTENTE",
                responsavel=self.responsavel
            )
    
    def test_responsavel_invalido(self):
        """Testa validação de responsável inválido."""
        with self.assertRaises(ValueError):
            BombonaFactory.criar_bombona(
                codigo="BQ001",
                volume=50.5,
                tipo_residuo="ÁCIDO",
                responsavel=None
            )


def executar_testes():
    """Executa todos os testes."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    executar_testes()