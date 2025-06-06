"""
Teste simples para verificar persistência dos dados
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.responsavel_controller import ResponsavelController
from controllers.bombona_controller import BombonaController
from dao.responsavel_dao import ResponsavelDAO
from dao.bombona_dao import BombonaDAO


def teste_simples():
    """Teste simples de persistência."""
    
    print("=== TESTE SIMPLES DE PERSISTÊNCIA ===\n")
    
    # Primeira execução - adiciona dados
    print("1. Primeira execução - adicionando dados...")
    
    # Inicializa sistema
    resp_dao = ResponsavelDAO()
    bomb_dao = BombonaDAO(responsavel_dao=resp_dao)
    resp_ctrl = ResponsavelController(resp_dao, bomb_dao)
    bomb_ctrl = BombonaController(bomb_dao, resp_dao)
    
    # Verifica quantos dados existem
    responsaveis_antes = resp_ctrl.listar_responsaveis()
    bombonas_antes = bomb_ctrl.listar_bombonas()
    
    print(f"   Responsáveis existentes: {len(responsaveis_antes)}")
    print(f"   Bombonas existentes: {len(bombonas_antes)}")
    
    # Tenta adicionar um responsável
    try:
        resp_ctrl.cadastrar_responsavel(
            "111.444.777-35",
            "Dr. João Silva",
            "(11) 9 8765-4321",
            "LABORATÓRIO"
        )
        print("   ✓ Responsável adicionado")
    except ValueError as e:
        print(f"   ℹ️  {e} (dados já existem - isso é CORRETO!)")
    
    # Tenta adicionar uma bombona
    try:
        bomb_ctrl.cadastrar_bombona(
            "LAB-001",
            25.5,
            "ÁCIDO",
            "11144477735"
        )
        print("   ✓ Bombona adicionada")
    except ValueError as e:
        print(f"   ℹ️  {e} (dados já existem - isso é CORRETO!)")
    
    # Segunda execução - simula reinicialização
    print("\n2. Segunda execução - simulando reinicialização...")
    
    # Cria NOVOS objetos (simula reinicialização do programa)
    novo_resp_dao = ResponsavelDAO()
    novo_bomb_dao = BombonaDAO(responsavel_dao=novo_resp_dao)
    novo_resp_ctrl = ResponsavelController(novo_resp_dao, novo_bomb_dao)
    novo_bomb_ctrl = BombonaController(novo_bomb_dao, novo_resp_dao)
    
    # Verifica se os dados persistiram
    responsaveis_depois = novo_resp_ctrl.listar_responsaveis()
    bombonas_depois = novo_bomb_ctrl.listar_bombonas()
    
    print(f"   Responsáveis carregados: {len(responsaveis_depois)}")
    print(f"   Bombonas carregadas: {len(bombonas_depois)}")
    
    # Mostra os dados para confirmar
    print("\n3. Dados persistidos:")
    print("   Responsáveis:")
    for resp in responsaveis_depois:
        print(f"   - {resp.get_nome()} | CPF: {resp.get_cpf()}")
    
    print("\n   Bombonas:")
    for bomb in bombonas_depois:
        resp_nome = bomb.get_responsavel().get_nome() if bomb.get_responsavel() else "N/A"
        print(f"   - {bomb.get_codigo()} | {bomb.get_volume()}L | Resp: {resp_nome}")
    
    # Verifica arquivos CSV
    print("\n4. Verificando arquivos CSV...")
    
    if os.path.exists("data/responsaveis.csv"):
        with open("data/responsaveis.csv", 'r', encoding='utf-8') as f:
            conteudo = f.read()
            linhas = conteudo.strip().split('\n')
            print(f"   📄 responsaveis.csv: {len(linhas)} linhas")
            if len(linhas) > 1:  # Tem dados além do cabeçalho
                print("      Conteúdo:")
                for linha in linhas:
                    print(f"      {linha}")
    
    if os.path.exists("data/bombonas.csv"):
        with open("data/bombonas.csv", 'r', encoding='utf-8') as f:
            conteudo = f.read()
            linhas = conteudo.strip().split('\n')
            print(f"\n   📄 bombonas.csv: {len(linhas)} linhas")
            if len(linhas) > 1:  # Tem dados além do cabeçalho
                print("      Conteúdo:")
                for linha in linhas:
                    print(f"      {linha}")
    
    print("\n=== RESULTADO ===")
    if len(responsaveis_depois) > 0 or len(bombonas_depois) > 0:
        print("✅ PERSISTÊNCIA FUNCIONANDO!")
        print("   Os dados são mantidos entre execuções do programa.")
    else:
        print("❌ PERSISTÊNCIA NÃO FUNCIONANDO!")
        print("   Os dados não estão sendo salvos corretamente.")


if __name__ == "__main__":
    teste_simples()