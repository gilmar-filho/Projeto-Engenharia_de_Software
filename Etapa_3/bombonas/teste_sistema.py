"""
Script para testar o sistema completo e demonstrar persistência dos CSVs
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dao.responsavel_dao import ResponsavelDAO
from dao.bombona_dao import BombonaDAO
from controllers.responsavel_controller import ResponsavelController
from controllers.bombona_controller import BombonaController


def verificar_arquivos_existentes():
    """Verifica se já existem dados nos arquivos CSV."""
    
    print("=== VERIFICAÇÃO DE DADOS EXISTENTES ===\n")
    
    # Verifica responsaveis.csv
    arquivo_resp = "data/responsaveis.csv"
    if os.path.exists(arquivo_resp):
        with open(arquivo_resp, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            dados = len(linhas) - 1  # Subtrai cabeçalho
            print(f"   📄 {arquivo_resp}: {dados} responsável(is) encontrado(s)")
    else:
        print(f"   📄 {arquivo_resp}: Arquivo não existe")
    
    # Verifica bombonas.csv
    arquivo_bomb = "data/bombonas.csv"
    if os.path.exists(arquivo_bomb):
        with open(arquivo_bomb, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            dados = len(linhas) - 1  # Subtrai cabeçalho
            print(f"   📄 {arquivo_bomb}: {dados} bombona(s) encontrada(s)")
    else:
        print(f"   📄 {arquivo_bomb}: Arquivo não existe")
    
    print()


def testar_persistencia():
    """Testa a persistência dos dados."""
    
    print("=== TESTE DE PERSISTÊNCIA DOS DADOS ===\n")
    
    try:
        # 1. Inicializar DAOs e Controllers
        print("1. Inicializando sistema...")
        responsavel_dao = ResponsavelDAO()
        bombona_dao = BombonaDAO(responsavel_dao=responsavel_dao)
        responsavel_controller = ResponsavelController(responsavel_dao, bombona_dao)
        bombona_controller = BombonaController(bombona_dao, responsavel_dao)
        
        # 2. Verificar dados existentes antes de adicionar
        print("\n2. Verificando dados já existentes...")
        responsaveis_existentes = responsavel_controller.listar_responsaveis()
        bombonas_existentes = bombona_controller.listar_bombonas()
        
        print(f"   Responsáveis já cadastrados: {len(responsaveis_existentes)}")
        print(f"   Bombonas já cadastradas: {len(bombonas_existentes)}")
        
        # 3. Adicionar novos dados (se não existirem)
        print("\n3. Adicionando novos dados...")
        
        # Lista de responsáveis para testar
        responsaveis_teste = [
            {
                "cpf": "111.444.777-35",
                "nome": "Dr. João Silva",
                "telefone": "(11) 9 8765-4321",
                "setor": "LABORATÓRIO"
            },
            {
                "cpf": "529.982.247-25",
                "nome": "Dra. Maria Santos",
                "telefone": "(11) 9 9999-8888",
                "setor": "QUÍMICA"
            }
        ]
        
        # Tentar cadastrar responsáveis
        for resp_data in responsaveis_teste:
            try:
                sucesso = responsavel_controller.cadastrar_responsavel(
                    resp_data["cpf"],
                    resp_data["nome"],
                    resp_data["telefone"],
                    resp_data["setor"]
                )
                if sucesso:
                    print(f"   ✓ Responsável {resp_data['nome']} cadastrado")
            except ValueError as e:
                if "Já existe" in str(e):
                    print(f"   ℹ️  Responsável {resp_data['nome']} já existe (CORRETO - dados persistentes!)")
                else:
                    print(f"   ✗ Erro ao cadastrar {resp_data['nome']}: {e}")
            except Exception as e:
                print(f"   ✗ Erro inesperado: {e}")
        
        # Lista de bombonas para testar
        bombonas_teste = [
            {
                "codigo": "LAB-001",
                "volume": 25.5,
                "tipo_residuo": "ÁCIDO",
                "cpf": "11144477735"  # Dr. João Silva
            },
            {
                "codigo": "QUI-001",
                "volume": 50.0,
                "tipo_residuo": "BASE",
                "cpf": "52998224725"  # Dra. Maria Santos
            }
        ]
        
        # Tentar cadastrar bombonas
        for bomb_data in bombonas_teste:
            try:
                sucesso = bombona_controller.cadastrar_bombona(
                    bomb_data["codigo"],
                    bomb_data["volume"],
                    bomb_data["tipo_residuo"],
                    bomb_data["cpf"]
                )
                if sucesso:
                    print(f"   ✓ Bombona {bomb_data['codigo']} cadastrada")
            except ValueError as e:
                if "Já existe" in str(e):
                    print(f"   ℹ️  Bombona {bomb_data['codigo']} já existe (CORRETO - dados persistentes!)")
                elif "não encontrado" in str(e):
                    print(f"   ⚠️  Responsável não encontrado para bombona {bomb_data['codigo']}")
                else:
                    print(f"   ✗ Erro ao cadastrar {bomb_data['codigo']}: {e}")
            except Exception as e:
                print(f"   ✗ Erro inesperado: {e}")
        
        # 4. Verificar dados após tentativa de inserção
        print("\n4. Verificando dados após inserção...")
        responsaveis_finais = responsavel_controller.listar_responsaveis()
        bombonas_finais = bombona_controller.listar_bombonas()
        
        print(f"   Total de responsáveis: {len(responsaveis_finais)}")
        for resp in responsaveis_finais:
            cpf_formatado = responsavel_controller.formatar_cpf_para_exibicao(resp.get_cpf())
            print(f"   - {resp.get_nome()} | CPF: {cpf_formatado} | Setor: {resp.get_setor()}")
        
        print(f"\n   Total de bombonas: {len(bombonas_finais)}")
        for bomb in bombonas_finais:
            responsavel = bomb.get_responsavel()
            resp_nome = responsavel.get_nome() if responsavel else "N/A"
            print(f"   - {bomb.get_codigo()} | {bomb.get_volume()}L | {bomb.get_tipo_residuo()} | Resp: {resp_nome}")
        
        # 5. Testar persistência reinicializando o sistema
        print("\n5. Testando persistência - reinicializando sistema...")
        
        # Simula reinicialização criando novos objetos
        novo_responsavel_dao = ResponsavelDAO()
        novo_bombona_dao = BombonaDAO(responsavel_dao=novo_responsavel_dao)
        novo_responsavel_controller = ResponsavelController(novo_responsavel_dao, novo_bombona_dao)
        novo_bombona_controller = BombonaController(novo_bombona_dao, novo_responsavel_dao)
        
        # Verifica se os dados persistiram
        responsaveis_persistidos = novo_responsavel_controller.listar_responsaveis()
        bombonas_persistidas = novo_bombona_controller.listar_bombonas()
        
        print(f"   Responsáveis carregados após reinicialização: {len(responsaveis_persistidos)}")
        print(f"   Bombonas carregadas após reinicialização: {len(bombonas_persistidas)}")
        
        if len(responsaveis_persistidos) == len(responsaveis_finais) and len(bombonas_persistidas) == len(bombonas_finais):
            print("   ✅ PERSISTÊNCIA FUNCIONANDO CORRETAMENTE!")
        else:
            print("   ❌ PROBLEMA NA PERSISTÊNCIA!")
        
        # 6. Gerar estatísticas
        print("\n6. Estatísticas do sistema...")
        stats_bombonas = novo_bombona_controller.get_estatisticas()
        stats_responsaveis = novo_responsavel_controller.get_estatisticas()
        
        print(f"   📊 Total de bombonas: {stats_bombonas['total_bombonas']}")
        print(f"   📊 Volume total: {stats_bombonas['volume_total']} L")
        print(f"   📊 Total de responsáveis: {stats_responsaveis['total_responsaveis']}")
        
        # 7. Testar operações CRUD
        print("\n7. Testando operações CRUD...")
        
        # Tentar buscar um responsável específico
        responsavel_teste = novo_responsavel_controller.buscar_responsavel("11144477735")
        if responsavel_teste:
            print(f"   🔍 Busca responsável: {responsavel_teste.get_nome()} encontrado")
            
            # Buscar bombonas deste responsável
            bombonas_resp = novo_bombona_controller.buscar_bombonas_por_cpf_responsavel("11144477735")
            print(f"   🔍 Bombonas deste responsável: {len(bombonas_resp)}")
        else:
            print("   🔍 Responsável de teste não encontrado")
        
        print("\n=== TESTE DE PERSISTÊNCIA CONCLUÍDO ===")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()


def demonstrar_adicao_incremental():
    """Demonstra que novos dados são adicionados aos existentes."""
    
    print("\n=== DEMONSTRAÇÃO DE ADIÇÃO INCREMENTAL ===\n")
    
    try:
        # Inicializa sistema
        responsavel_dao = ResponsavelDAO()
        bombona_dao = BombonaDAO(responsavel_dao=responsavel_dao)
        responsavel_controller = ResponsavelController(responsavel_dao, bombona_dao)
        bombona_controller = BombonaController(bombona_dao, responsavel_dao)
        
        # Conta dados atuais
        responsaveis_antes = len(responsavel_controller.listar_responsaveis())
        bombonas_antes = len(bombona_controller.listar_bombonas())
        
        print(f"Dados ANTES da adição:")
        print(f"   Responsáveis: {responsaveis_antes}")
        print(f"   Bombonas: {bombonas_antes}")
        
        # Tenta adicionar um novo responsável único
        import time
        timestamp = str(int(time.time()))[-4:]  # Últimos 4 dígitos do timestamp
        
        try:
            novo_cpf = f"111.222.333-9{timestamp[-1]}"  # CPF único baseado no timestamp
            # Gera um CPF válido simples para teste
            if timestamp[-1] == "0":
                novo_cpf = "11122233396"
            elif timestamp[-1] == "1":
                novo_cpf = "22233344407"
            elif timestamp[-1] == "2":
                novo_cpf = "33344455518"
            else:
                novo_cpf = "44455566629"
            
            sucesso = responsavel_controller.cadastrar_responsavel(
                novo_cpf,
                f"Novo Responsável {timestamp}",
                "11999999999",
                "OUTROS"
            )
            
            if sucesso:
                print(f"\n✓ Novo responsável adicionado: Novo Responsável {timestamp}")
                
                # Tenta adicionar uma bombona para este responsável
                sucesso_bomb = bombona_controller.cadastrar_bombona(
                    f"TEST-{timestamp}",
                    10.0,
                    "OUTROS",
                    novo_cpf.replace(".", "").replace("-", "")
                )
                
                if sucesso_bomb:
                    print(f"✓ Nova bombona adicionada: TEST-{timestamp}")
        
        except Exception as e:
            print(f"ℹ️  Dados já existem ou erro esperado: {e}")
        
        # Conta dados depois
        responsaveis_depois = len(responsavel_controller.listar_responsaveis())
        bombonas_depois = len(bombona_controller.listar_bombonas())
        
        print(f"\nDados DEPOIS da tentativa de adição:")
        print(f"   Responsáveis: {responsaveis_depois}")
        print(f"   Bombonas: {bombonas_depois}")
        
        print(f"\nVariação:")
        print(f"   Responsáveis: +{responsaveis_depois - responsaveis_antes}")
        print(f"   Bombonas: +{bombonas_depois - bombonas_antes}")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")


def main():
    """Função principal."""
    
    # Verifica dados existentes
    verificar_arquivos_existentes()
    
    # Testa persistência
    testar_persistencia()
    
    # Demonstra adição incremental
    demonstrar_adicao_incremental()
    
    print("\n" + "="*60)
    print("🎯 RESUMO:")
    print("• Os dados agora são PERSISTENTES entre execuções")
    print("• Novos dados são ADICIONADOS aos existentes")
    print("• CSVs mantêm o histórico de todas as operações")
    print("• Execute 'python main.py' para usar a interface gráfica")
    print("="*60)


if __name__ == "__main__":
    main()
    """
    Script para testar o sistema completo e popular os CSVs
    """

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dao.responsavel_dao import ResponsavelDAO
from dao.bombona_dao import BombonaDAO
from controllers.responsavel_controller import ResponsavelController
from controllers.bombona_controller import BombonaController


def teste_completo_sistema():
    """Testa o sistema completo e popula os CSVs."""
    
    print("=== TESTE COMPLETO DO SISTEMA ===\n")
    
    try:
        # 1. Inicializar DAOs
        print("1. Inicializando DAOs...")
        responsavel_dao = ResponsavelDAO()
        bombona_dao = BombonaDAO(responsavel_dao=responsavel_dao)
        
        # 2. Inicializar Controllers
        print("2. Inicializando Controllers...")
        responsavel_controller = ResponsavelController(responsavel_dao, bombona_dao)
        bombona_controller = BombonaController(bombona_dao, responsavel_dao)
        
        # 3. Cadastrar alguns responsáveis
        print("\n3. Cadastrando responsáveis...")
        
        responsaveis_teste = [
            {
                "cpf": "111.444.777-35",
                "nome": "Dr. João Silva",
                "telefone": "(11) 9 8765-4321",
                "setor": "LABORATÓRIO"
            },
            {
                "cpf": "529.982.247-25",
                "nome": "Dra. Maria Santos",
                "telefone": "(11) 9 9999-8888",
                "setor": "QUÍMICA"
            },
            {
                "cpf": "123.456.789-09",
                "nome": "Prof. Carlos Oliveira",
                "telefone": "(11) 9 7777-6666",
                "setor": "BIOLOGIA"
            },
            {
                "cpf": "987.654.321-00",
                "nome": "Ana Costa Lima",
                "telefone": "(11) 9 5555-4444",
                "setor": "FÍSICA"
            }
        ]
        
        for resp_data in responsaveis_teste:
            try:
                sucesso = responsavel_controller.cadastrar_responsavel(
                    resp_data["cpf"],
                    resp_data["nome"],
                    resp_data["telefone"],
                    resp_data["setor"]
                )
                if sucesso:
                    print(f"   ✓ Responsável {resp_data['nome']} cadastrado com sucesso")
                else:
                    print(f"   ✗ Erro ao cadastrar {resp_data['nome']}")
            except Exception as e:
                print(f"   ✗ Erro ao cadastrar {resp_data['nome']}: {e}")
        
        # 4. Listar responsáveis cadastrados
        print("\n4. Listando responsáveis cadastrados...")
        responsaveis = responsavel_controller.listar_responsaveis()
        print(f"   Total de responsáveis: {len(responsaveis)}")
        for resp in responsaveis:
            cpf_formatado = responsavel_controller.formatar_cpf_para_exibicao(resp.get_cpf())
            tel_formatado = responsavel_controller.formatar_telefone_para_exibicao(resp.get_telefone())
            print(f"   - {resp.get_nome()} | CPF: {cpf_formatado} | Tel: {tel_formatado} | Setor: {resp.get_setor()}")
        
        # 5. Cadastrar algumas bombonas
        print("\n5. Cadastrando bombonas...")
        
        bombonas_teste = [
            {
                "codigo": "LAB-001",
                "volume": 25.5,
                "tipo_residuo": "ÁCIDO",
                "cpf": "11144477735"  # Dr. João Silva
            },
            {
                "codigo": "LAB-002",
                "volume": 50.0,
                "tipo_residuo": "BASE",
                "cpf": "11144477735"  # Dr. João Silva
            },
            {
                "codigo": "QUI-001",
                "volume": 75.5,
                "tipo_residuo": "SOLVENTE",
                "cpf": "52998224725"  # Dra. Maria Santos
            },
            {
                "codigo": "BIO-001",
                "volume": 30.0,
                "tipo_residuo": "ORGÂNICO",
                "cpf": "12345678909"  # Prof. Carlos Oliveira
            },
            {
                "codigo": "FIS-001",
                "volume": 100.0,
                "tipo_residuo": "METAL PESADO",
                "cpf": "98765432100"  # Ana Costa Lima
            },
            {
                "codigo": "LAB-003",
                "volume": 15.0,
                "tipo_residuo": "INFLAMÁVEL",
                "cpf": "11144477735"  # Dr. João Silva
            }
        ]
        
        for bomb_data in bombonas_teste:
            try:
                sucesso = bombona_controller.cadastrar_bombona(
                    bomb_data["codigo"],
                    bomb_data["volume"],
                    bomb_data["tipo_residuo"],
                    bomb_data["cpf"]
                )
                if sucesso:
                    print(f"   ✓ Bombona {bomb_data['codigo']} cadastrada com sucesso")
                else:
                    print(f"   ✗ Erro ao cadastrar {bomb_data['codigo']}")
            except Exception as e:
                print(f"   ✗ Erro ao cadastrar {bomb_data['codigo']}: {e}")
        
        # 6. Listar bombonas cadastradas
        print("\n6. Listando bombonas cadastradas...")
        bombonas = bombona_controller.listar_bombonas()
        print(f"   Total de bombonas: {len(bombonas)}")
        for bomb in bombonas:
            responsavel = bomb.get_responsavel()
            resp_nome = responsavel.get_nome() if responsavel else "N/A"
            print(f"   - {bomb.get_codigo()} | {bomb.get_volume()}L | {bomb.get_tipo_residuo()} | Resp: {resp_nome}")
        
        # 7. Testar busca por responsável
        print("\n7. Testando busca de bombonas por responsável...")
        cpf_teste = "11144477735"  # Dr. João Silva
        bombonas_responsavel = bombona_controller.buscar_bombonas_por_cpf_responsavel(cpf_teste)
        print(f"   Bombonas do Dr. João Silva: {len(bombonas_responsavel)}")
        for bomb in bombonas_responsavel:
            print(f"   - {bomb.get_codigo()} | {bomb.get_volume()}L | {bomb.get_tipo_residuo()}")
        
        # 8. Gerar estatísticas
        print("\n8. Gerando estatísticas...")
        stats_bombonas = bombona_controller.get_estatisticas()
        stats_responsaveis = responsavel_controller.get_estatisticas()
        
        print(f"   Total de bombonas: {stats_bombonas['total_bombonas']}")
        print(f"   Volume total: {stats_bombonas['volume_total']} L")
        print(f"   Volume médio: {stats_bombonas['volume_medio']} L")
        print(f"   Total de responsáveis: {stats_responsaveis['total_responsaveis']}")
        
        print("\n   Bombonas por tipo de resíduo:")
        for tipo, qtd in stats_bombonas['tipos_residuo'].items():
            print(f"   - {tipo}: {qtd}")
        
        print("\n   Responsáveis por setor:")
        for setor, qtd in stats_responsaveis['responsaveis_por_setor'].items():
            print(f"   - {setor}: {qtd}")
        
        # 9. Gerar relatórios
        print("\n9. Gerando relatórios...")
        try:
            arquivo_csv = bombona_controller.gerar_relatorio("csv")
            print(f"   ✓ Relatório CSV gerado: {arquivo_csv}")
            
            arquivo_txt = bombona_controller.gerar_relatorio("txt")
            print(f"   ✓ Relatório TXT gerado: {arquivo_txt}")
        except Exception as e:
            print(f"   ✗ Erro ao gerar relatórios: {e}")
        
        # 10. Verificar arquivos CSV
        print("\n10. Verificando arquivos CSV...")
        
        # Verifica responsaveis.csv
        if os.path.exists("data/responsaveis.csv"):
            with open("data/responsaveis.csv", 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                print(f"   ✓ responsaveis.csv criado com {len(linhas)} linhas")
        else:
            print("   ✗ responsaveis.csv não encontrado")
        
        # Verifica bombonas.csv
        if os.path.exists("data/bombonas.csv"):
            with open("data/bombonas.csv", 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                print(f"   ✓ bombonas.csv criado com {len(linhas)} linhas")
        else:
            print("   ✗ bombonas.csv não encontrado")
        
        print("\n=== TESTE CONCLUÍDO COM SUCESSO! ===")
        print("\nOs arquivos CSV agora devem estar populados com dados de teste.")
        print("Você pode executar 'python main.py' para ver a interface gráfica.")
        
    except Exception as e:
        print(f"\n✗ ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()


def limpar_dados():
    """Limpa os dados existentes (para recriar do zero)."""
    
    print("=== LIMPANDO DADOS EXISTENTES ===")
    
    arquivos = [
        "data/responsaveis.csv",
        "data/bombonas.csv",
        "data/relatorio_bombonas.csv",
        "data/relatorio_bombonas.txt"
    ]
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"   ✓ Arquivo {arquivo} removido")
        else:
            print(f"   - Arquivo {arquivo} não existe")
    
    print("   Dados limpos!\n")


def main():
    """Função principal."""
    
    # Pergunta se quer limpar dados primeiro
    resposta = input("Deseja limpar os dados existentes antes do teste? (s/n): ").lower().strip()
    if resposta in ['s', 'sim', 'y', 'yes']:
        limpar_dados()
    
    # Executa o teste completo
    teste_completo_sistema()


if __name__ == "__main__":
    main()