"""
Testes E2E Simplificados - Simulando Cypress
Sistema de Gerenciamento de Bombonas de Resíduos Químicos

Arquivo único com todos os testes end-to-end
Simula o comportamento do Cypress para aplicações desktop Tkinter
"""

import pyautogui
import subprocess
import time
import os
import sys
from pathlib import Path
from datetime import datetime
import random

# ==================== CONFIGURAÇÃO GLOBAL ====================

# Diretórios
DIRETORIO_PROJETO = Path(__file__).parent.parent
DIRETORIO_SCREENSHOTS = Path(__file__).parent / "screenshots"
DIRETORIO_RELATORIOS = Path(__file__).parent / "relatorios"

# Cria pastas se não existirem
DIRETORIO_SCREENSHOTS.mkdir(exist_ok=True)
DIRETORIO_RELATORIOS.mkdir(exist_ok=True)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True  
pyautogui.PAUSE = 1.0  

# Arquivo de relatório
arquivo_relatorio = None
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# ==================== UTILITÁRIOS DE RELATÓRIO ====================

def iniciar_relatorio(nome_secao=""):
    """Inicia o arquivo de relatório de testes"""
    global arquivo_relatorio, total_testes, testes_passaram, testes_falharam
    
    # Reseta contadores
    total_testes = 0
    testes_passaram = 0
    testes_falharam = 0
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = DIRETORIO_RELATORIOS / f"relatorio_{nome_secao}_{timestamp}.txt"
    
    arquivo_relatorio = open(nome_arquivo, 'w', encoding='utf-8')
    
    escrever_relatorio("=" * 70)
    escrever_relatorio("RELATÓRIO DE TESTES E2E - SISTEMA DE BOMBONAS")
    if nome_secao:
        escrever_relatorio(f"Seção: {nome_secao}")
    escrever_relatorio("=" * 70)
    escrever_relatorio(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    escrever_relatorio(f"Simulando comportamento do Cypress para Tkinter")
    escrever_relatorio("=" * 70)
    escrever_relatorio("")
    
    return nome_arquivo

def escrever_relatorio(texto):
    """Escreve no arquivo de relatório e no console"""
    print(texto)
    if arquivo_relatorio:
        arquivo_relatorio.write(texto + "\n")
        arquivo_relatorio.flush()

def fechar_relatorio():
    """Fecha o arquivo de relatório com resumo final"""
    global arquivo_relatorio
    
    if arquivo_relatorio:
        escrever_relatorio("")
        escrever_relatorio("=" * 70)
        escrever_relatorio("RESUMO FINAL DOS TESTES")
        escrever_relatorio("=" * 70)
        escrever_relatorio(f"Total de testes executados: {total_testes}")
        escrever_relatorio(f"Testes aprovados: {testes_passaram}")
        escrever_relatorio(f"Testes reprovados: {testes_falharam}")
        escrever_relatorio(f"Taxa de sucesso: {(testes_passaram/total_testes*100):.1f}%" if total_testes > 0 else "0%")
        escrever_relatorio("=" * 70)
        
        arquivo_relatorio.close()

def registrar_teste(nome_teste, sucesso, mensagem=""):
    """Registra o resultado de um teste"""
    global total_testes, testes_passaram, testes_falharam
    
    total_testes += 1
    if sucesso:
        testes_passaram += 1
        escrever_relatorio(f"[PASSOU] {nome_teste}")
    else:
        testes_falharam += 1
        escrever_relatorio(f"[FALHOU] {nome_teste}")
        if mensagem:
            escrever_relatorio(f"         Erro: {mensagem}")

# ==================== UTILITÁRIOS BÁSICOS ====================

def iniciar_aplicacao():
    """Inicia a aplicação"""
    escrever_relatorio("Iniciando aplicação...")
    
    processo = subprocess.Popen([sys.executable, str(DIRETORIO_PROJETO / "main.py")])
    time.sleep(4)
    
    escrever_relatorio("Aplicação iniciada")
    return processo

def parar_aplicacao(processo):
    """Para a aplicação"""
    escrever_relatorio("Parando aplicação...")
    
    try:
        processo.terminate()
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        escrever_relatorio("Forçando encerramento...")
        processo.kill()
    
    time.sleep(1)
    escrever_relatorio("Aplicação parada")

def clicar_imagem(nome_imagem, confianca=0.8, timeout=5):
    """Clica em uma imagem na tela"""
    caminho_imagem = DIRETORIO_SCREENSHOTS / nome_imagem
    
    if not caminho_imagem.exists():
        escrever_relatorio(f"Imagem não encontrada: {caminho_imagem}")
        return False
    
    escrever_relatorio(f"Procurando por: {nome_imagem}")
    
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        try:
            localizacao = pyautogui.locateOnScreen(str(caminho_imagem), confidence=confianca)
            if localizacao:
                centro = pyautogui.center(localizacao)
                pyautogui.click(centro)
                escrever_relatorio(f"Clicou em: {nome_imagem}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            escrever_relatorio(f"Erro ao procurar imagem: {e}")
        
        time.sleep(0.5)
    
    escrever_relatorio(f"Imagem não encontrada após {timeout}s: {nome_imagem}")
    return False

def selecionar_item_aleatorio_lista():
    """Seleciona um item aleatório da lista usando as setas"""
    escrever_relatorio("Selecionando item aleatório da lista...")
    
    # Número aleatório de setas para baixo (entre 0 e 4)
    quantidade_setas = random.randint(0, 4)
    
    for i in range(quantidade_setas):
        pressionar_tecla("down")
        time.sleep(0.2)
    
    # Pressiona espaço para selecionar
    pressionar_tecla("space")
    time.sleep(0.5)
    
    return True

def digitar_texto(texto, intervalo=0.1):
    """Digita texto"""
    escrever_relatorio(f"Digitando: {texto}")
    pyautogui.write(texto, interval=intervalo)

def pressionar_tecla(tecla):
    """Pressiona uma tecla"""
    escrever_relatorio(f"Pressionando: {tecla}")
    pyautogui.press(tecla)

def aguardar_imagem(nome_imagem, timeout=10, confianca=0.8):
    """Aguarda uma imagem aparecer na tela"""
    caminho_imagem = DIRETORIO_SCREENSHOTS / nome_imagem
    
    if not caminho_imagem.exists():
        escrever_relatorio(f"Imagem não encontrada: {caminho_imagem}")
        return False
    
    escrever_relatorio(f"Aguardando: {nome_imagem} (timeout: {timeout}s)")
    
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        try:
            localizacao = pyautogui.locateOnScreen(str(caminho_imagem), confidence=confianca)
            if localizacao:
                escrever_relatorio(f"Imagem encontrada: {nome_imagem}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            escrever_relatorio(f"Erro ao aguardar imagem: {e}")
        
        time.sleep(0.5)
    
    escrever_relatorio(f"Timeout aguardando: {nome_imagem}")
    return False

def verificar_imagem_visivel(nome_imagem, confianca=0.8):
    """Verifica se uma imagem está visível"""
    caminho_imagem = DIRETORIO_SCREENSHOTS / nome_imagem
    
    if not caminho_imagem.exists():
        escrever_relatorio(f"Imagem não encontrada: {caminho_imagem}")
        return False
    
    try:
        localizacao = pyautogui.locateOnScreen(str(caminho_imagem), confidence=confianca)
        visivel = localizacao is not None
        
        if visivel:
            escrever_relatorio(f"Imagem visível: {nome_imagem}")
        else:
            escrever_relatorio(f"Imagem não visível: {nome_imagem}")
        
        return visivel
    except Exception as e:
        escrever_relatorio(f"Erro ao verificar imagem: {e}")
        return False

def fazer_login(usuario="admin", senha="123456"):
    """Realiza login"""
    escrever_relatorio(f"Realizando login com usuário: {usuario}")
    
    if not aguardar_imagem("login_screen.png", timeout=10):
        return False
    
    digitar_texto(usuario)
    pressionar_tecla("tab")
    digitar_texto(senha)
    pressionar_tecla("enter")
    
    return aguardar_imagem("main_interface.png", timeout=10)

def fechar_dialogos():
    """Fecha diálogos que possam estar abertos"""
    escrever_relatorio("Fechando possíveis diálogos...")
    
    # Primeiro tenta com ESC (fecha sem confirmar)
    pressionar_tecla("escape")
    time.sleep(0.5)
    
    # Se ainda houver diálogo, usa Tab + Enter para selecionar "Não"
    if verificar_imagem_visivel("dialog_box.png", confianca=0.7):
        pressionar_tecla("tab")
        time.sleep(0.2)
        pressionar_tecla("enter")
        time.sleep(0.5)

def limpar_campos_formulario(quantidade_tabs):
    """Limpa campos do formulário usando Ctrl+A e Delete"""
    for i in range(quantidade_tabs):
        pyautogui.hotkey('ctrl', 'a')
        pressionar_tecla('delete')
        pressionar_tecla('tab')

# ==================== TESTES DE LOGIN ====================

class TestesLogin:
    """Testes do fluxo de login"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de login"""
        self.testar_exibir_tela_login()
        self.testar_login_credenciais_validas()
        self.testar_rejeitar_credenciais_invalidas()
        self.testar_login_campos_vazios()
    
    def testar_exibir_tela_login(self):
        """Deve exibir a tela de login ao iniciar a aplicação"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Exibir tela de login")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            sucesso = aguardar_imagem("login_screen.png", timeout=10)
            registrar_teste(
                "Exibir tela de login",
                sucesso,
                "Tela de login não apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_credenciais_validas(self):
        """Deve fazer login com credenciais válidas"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Login com credenciais válidas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            sucesso = fazer_login()
            registrar_teste(
                "Login com credenciais válidas",
                sucesso,
                "Login não foi realizado com sucesso" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_credenciais_invalidas(self):
        """Deve rejeitar credenciais inválidas"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar credenciais inválidas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            digitar_texto("Joao Silva Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("LABORATORIO")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Criar responsável com dados válidos",
                sucesso,
                "Mensagem de sucesso não apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_cpf_invalido(self):
        """Deve rejeitar CPF inválido"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar CPF inválido")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("11111111111")
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar CPF inválido (dígitos iguais)",
                sucesso,
                "Deveria rejeitar CPF com todos dígitos iguais" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_cpf_tamanho_incorreto(self):
        """Deve rejeitar CPF com tamanho incorreto"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar CPF com tamanho incorreto")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("123456789")
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar CPF com menos de 11 dígitos",
                sucesso,
                "Deveria rejeitar CPF com tamanho incorreto" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_campos_vazios_responsavel(self):
        """Deve rejeitar cadastro com campos vazios"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar campos vazios no cadastro de responsável")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro com campos vazios",
                sucesso,
                "Deveria rejeitar cadastro sem dados" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE LISTAGEM DE RESPONSÁVEL ====================

class TestesListagemResponsavel:
    """Testes de listagem, edição e exclusão de responsáveis"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de listagem"""
        self.testar_listar_responsaveis()
        self.testar_editar_responsavel()
        self.testar_remover_responsavel_sem_bombonas()
        self.testar_validacao_edicao_responsavel()
    
    def testar_listar_responsaveis(self):
        """Deve listar responsáveis cadastrados"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Listar responsáveis")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("lista_responsaveis.png") or verificar_imagem_visivel("table_header.png")
            registrar_teste(
                "Listar responsáveis",
                sucesso,
                "Lista de responsáveis não apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel(self):
        """Deve editar um responsável existente"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Editar responsável")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Primeiro cria um responsável para editar
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("45678912305")  # CPF diferente para evitar duplicata
            pressionar_tecla("tab")
            digitar_texto("Maria Santos Original")
            pressionar_tecla("tab")
            digitar_texto("11988776655")
            pressionar_tecla("tab")
            digitar_texto("FINANCEIRO")
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Lista responsáveis
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Seleciona um item aleatório
            selecionar_item_aleatorio_lista()
            
            # Clica em editar
            if clicar_imagem("btn_editar.png"):
                time.sleep(1)
                
                # Edita o nome
                pressionar_tecla("tab")  # Pula CPF
                pyautogui.hotkey('ctrl', 'a')
                digitar_texto("Maria Santos Editada")
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Editar responsável",
                    sucesso,
                    "Não conseguiu editar responsável" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Editar responsável",
                    False,
                    "Botão editar não encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_remover_responsavel_sem_bombonas(self):
        """Deve remover responsável que não possui bombonas"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Remover responsável sem bombonas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Cria um responsável específico para remover
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("99988877766")  # CPF temporário
            pressionar_tecla("tab")
            digitar_texto("Teste Remocao Temp")
            pressionar_tecla("tab")
            digitar_texto("11977665544")
            pressionar_tecla("tab")
            digitar_texto("TEMPORARIO")
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Lista responsáveis
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Como sabemos que o último cadastrado está no final, navega até lá
            for i in range(10):
                pressionar_tecla("down")
                time.sleep(0.1)
            
            pressionar_tecla("space")  # Seleciona
            time.sleep(0.5)
            
            # Remove
            if clicar_imagem("btn_excluir.png"):
                time.sleep(1)
                
                # Confirma exclusão
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Remover responsável sem bombonas",
                    sucesso,
                    "Não conseguiu remover responsável" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Remover responsável sem bombonas",
                    False,
                    "Botão excluir não encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_validacao_edicao_responsavel(self):
        """Deve validar campos na edição de responsável"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Validar campos na edição de responsável")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Lista responsáveis
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Seleciona primeiro item
            pressionar_tecla("down")
            time.sleep(0.2)
            pressionar_tecla("space")
            time.sleep(0.5)
            
            # Edita
            if clicar_imagem("btn_editar.png"):
                time.sleep(1)
                
                # Tenta deixar o nome vazio
                pressionar_tecla("tab")  # Pula CPF
                pyautogui.hotkey('ctrl', 'a')
                pressionar_tecla('delete')
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Validar nome vazio na edição",
                    sucesso,
                    "Deveria rejeitar nome vazio na edição" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Validar nome vazio na edição",
                    False,
                    "Botão editar não encontrado"
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE CADASTRO DE BOMBONA ====================

class TestesCadastroBombona:
    """Testes de cadastro de bombonas"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de cadastro"""
        self.testar_criar_bombona_valida()
        self.testar_rejeitar_codigo_bombona_invalido()
        self.testar_rejeitar_volume_com_letras()
        self.testar_rejeitar_campos_vazios_bombona()
    
    def testar_criar_bombona_valida(self):
        """Deve criar uma nova bombona com dados válidos"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Criar bombona válida")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Cadastra bombona diretamente
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            digitar_texto("LAB-001")
            pressionar_tecla("tab")
            digitar_texto("50.5")
            pressionar_tecla("tab")
            pressionar_tecla("down")  # Seleciona primeiro tipo
            pressionar_tecla("tab")
            pressionar_tecla("down")  # Seleciona primeiro responsável disponível
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Criar bombona com dados válidos",
                sucesso,
                "Não conseguiu criar bombona" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_codigo_bombona_invalido(self):
        """Deve rejeitar código de bombona fora do padrão"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar código de bombona inválido")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            digitar_texto("12345")  # Código inválido
            pressionar_tecla("tab")
            digitar_texto("30")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar código de bombona inválido",
                sucesso,
                "Deveria rejeitar código fora do padrão LLL-NNN" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_volume_com_letras(self):
        """Deve rejeitar volume com letras"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar volume com letras")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            digitar_texto("ABC-123")
            pressionar_tecla("tab")
            digitar_texto("ABC")  # Volume com letras
            pressionar_tecla("tab")
            pressionar_tecla("down")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar volume com letras",
                sucesso,
                "Deveria rejeitar volume não numérico" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_campos_vazios_bombona(self):
        """Deve rejeitar cadastro de bombona com campos vazios"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar campos vazios no cadastro de bombona")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro de bombona sem dados",
                sucesso,
                "Deveria rejeitar cadastro sem preencher campos" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE LISTAGEM DE BOMBONA ====================

class TestesListagemBombona:
    """Testes de listagem, edição e exclusão de bombonas"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de listagem"""
        self.testar_listar_bombonas()
        self.testar_editar_bombona()
        self.testar_remover_bombona()
        self.testar_validacao_edicao_bombona()
    
    def testar_listar_bombonas(self):
        """Deve listar bombonas cadastradas"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Listar bombonas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_listar_bombonas.png")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("lista_bombonas.png") or verificar_imagem_visivel("table_header.png")
            registrar_teste(
                "Listar bombonas",
                sucesso,
                "Lista de bombonas não apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_bombona(self):
        """Deve editar uma bombona existente"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Editar bombona")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Lista bombonas
            clicar_imagem("btn_listar_bombonas.png")
            time.sleep(2)
            
            # Seleciona item aleatório
            selecionar_item_aleatorio_lista()
            
            # Clica em editar
            if clicar_imagem("btn_editar.png"):
                time.sleep(1)
                
                # Edita o volume
                pressionar_tecla("tab")  # Pula código
                pyautogui.hotkey('ctrl', 'a')
                digitar_texto("75.5")
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Editar bombona",
                    sucesso,
                    "Não conseguiu editar bombona" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Editar bombona",
                    False,
                    "Botão editar não encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_remover_bombona(self):
        """Deve remover uma bombona"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Remover bombona")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Lista bombonas
            clicar_imagem("btn_listar_bombonas.png")
            time.sleep(2)
            
            # Seleciona item aleatório
            selecionar_item_aleatorio_lista()
            
            # Remove
            if clicar_imagem("btn_excluir.png"):
                time.sleep(1)
                
                # Confirma exclusão
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Remover bombona",
                    sucesso,
                    "Não conseguiu remover bombona" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Remover bombona",
                    False,
                    "Botão excluir não encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_validacao_edicao_bombona(self):
        """Deve validar campos na edição de bombona"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Validar campos na edição de bombona")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Lista bombonas
            clicar_imagem("btn_listar_bombonas.png")
            time.sleep(2)
            
            # Seleciona primeiro item
            pressionar_tecla("down")
            time.sleep(0.2)
            pressionar_tecla("space")
            time.sleep(0.5)
            
            # Edita
            if clicar_imagem("btn_editar.png"):
                time.sleep(1)
                
                # Tenta colocar volume negativo
                pressionar_tecla("tab")  # Pula código
                pyautogui.hotkey('ctrl', 'a')
                digitar_texto("-50")
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Validar volume negativo na edição",
                    sucesso,
                    "Deveria rejeitar volume negativo na edição" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Validar volume negativo na edição",
                    False,
                    "Botão editar não encontrado"
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE INTEGRAÇÃO ====================

class TestesIntegracao:
    """Testes de integração entre módulos"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de integração"""
        self.testar_remover_responsavel_com_bombonas()
    
    def testar_remover_responsavel_com_bombonas(self):
        """Deve impedir remoção de responsável que possui bombonas"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Impedir remoção de responsável com bombonas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Cria responsável
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("77788899900")
            pressionar_tecla("tab")
            digitar_texto("Responsavel Com Bombona")
            pressionar_tecla("tab")
            digitar_texto("11955443322")
            pressionar_tecla("tab")
            digitar_texto("PRODUCAO")
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Cria bombona vinculada
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            digitar_texto("PRD-100")
            pressionar_tecla("tab")
            digitar_texto("100")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            pressionar_tecla("tab")
            
            # Navega até o último responsável
            for i in range(10):
                pressionar_tecla("down")
                time.sleep(0.1)
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Tenta remover o responsável
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Navega até o último (que foi criado)
            for i in range(10):
                pressionar_tecla("down")
                time.sleep(0.1)
            
            pressionar_tecla("space")
            time.sleep(0.5)
            
            if clicar_imagem("btn_excluir.png"):
                time.sleep(1)
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") and not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Impedir remoção de responsável com bombonas",
                    sucesso,
                    "Deveria impedir remoção de responsável com bombonas vinculadas" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Impedir remoção de responsável com bombonas",
                    False,
                    "Botão excluir não encontrado"
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE RELATÓRIOS ====================

class TestesRelatorios:
    """Testes de geração de relatórios"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de relatórios"""
        self.testar_geracao_relatorio_csv()
        self.testar_geracao_relatorio_pdf()
    
    def testar_geracao_relatorio_csv(self):
        """Deve gerar relatório em CSV"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Gerar relatório CSV")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            if clicar_imagem("btn_relatorios.png"):
                time.sleep(1)
                
                # Seleciona CSV se necessário
                if clicar_imagem("combo_formato.png", confianca=0.7):
                    time.sleep(0.5)
                    clicar_imagem("opcao_csv.png", confianca=0.7)
                    time.sleep(0.5)
                
                # Clica em gerar relatório de bombonas
                if clicar_imagem("btn_relatorio_bombonas.png"):
                    time.sleep(3)
                    
                    # Verifica se abriu diálogo de salvar
                    sucesso = aguardar_imagem("save_dialog.png", timeout=5)
                    if sucesso:
                        pressionar_tecla("escape")  # Cancela o salvamento
                        
                    registrar_teste(
                        "Gerar relatório CSV",
                        sucesso,
                        "Não abriu diálogo de salvamento" if not sucesso else ""
                    )
                else:
                    registrar_teste("Gerar relatório CSV", False, "Botão de relatório não encontrado")
            else:
                registrar_teste("Gerar relatório CSV", False, "Não conseguiu acessar tela de relatórios")
            
        finally:
            parar_aplicacao(app)
    
    def testar_geracao_relatorio_pdf(self):
        """Deve gerar relatório em PDF"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Gerar relatório PDF")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            if clicar_imagem("btn_relatorios.png"):
                time.sleep(1)
                
                # Seleciona PDF
                if clicar_imagem("combo_formato.png", confianca=0.7):
                    time.sleep(0.5)
                    clicar_imagem("opcao_pdf.png", confianca=0.7)
                    time.sleep(0.5)
                
                # Clica em gerar relatório
                if clicar_imagem("btn_relatorio_responsaveis.png"):
                    time.sleep(3)
                    
                    sucesso = aguardar_imagem("save_dialog.png", timeout=5)
                    if sucesso:
                        pressionar_tecla("escape")
                        
                    registrar_teste(
                        "Gerar relatório PDF",
                        sucesso,
                        "Não abriu diálogo de salvamento" if not sucesso else ""
                    )
                else:
                    registrar_teste("Gerar relatório PDF", False, "Botão de relatório não encontrado")
            else:
                registrar_teste("Gerar relatório PDF", False, "Não conseguiu acessar tela de relatórios")
            
        finally:
            parar_aplicacao(app)

# ==================== MENU DE TESTES ====================

def exibir_menu():
    """Exibe menu de seleção de testes"""
    print("\n" + "=" * 60)
    print("MENU DE TESTES E2E - SISTEMA DE BOMBONAS")
    print("=" * 60)
    print("1 - Testes de Login")
    print("2 - Testes de Cadastro de Responsável")
    print("3 - Testes de Listagem de Responsável")
    print("4 - Testes de Cadastro de Bombona")
    print("5 - Testes de Listagem de Bombona")
    print("6 - Testes de Integração")
    print("7 - Testes de Relatórios")
    print("8 - Executar TODOS os testes")
    print("0 - Sair")
    print("=" * 60)
    
    return input("Escolha uma opção: ")

def executar_opcao(opcao):
    """Executa a opção selecionada"""
    
    mapa_opcoes = {
        "1": ("Testes de Login", TestesLogin),
        "2": ("Testes de Cadastro de Responsável", TestesCadastroResponsavel),
        "3": ("Testes de Listagem de Responsável", TestesListagemResponsavel),
        "4": ("Testes de Cadastro de Bombona", TestesCadastroBombona),
        "5": ("Testes de Listagem de Bombona", TestesListagemBombona),
        "6": ("Testes de Integração", TestesIntegracao),
        "7": ("Testes de Relatórios", TestesRelatorios),
    }
    
    if opcao in mapa_opcoes:
        nome_secao, classe_teste = mapa_opcoes[opcao]
        
        # Inicia relatório para a seção específica
        nome_arquivo_relatorio = iniciar_relatorio(nome_secao.replace(" ", "_"))
        
        print(f"\nExecutando: {nome_secao}")
        print("-" * 60)
        
        # Executa os testes da classe
        instancia = classe_teste()
        instancia.executar_todos_testes()
        
        # Fecha relatório
        fechar_relatorio()
        
        print(f"\nRelatório salvo em: {nome_arquivo_relatorio}")
        print(f"Taxa de sucesso: {(testes_passaram/total_testes*100):.1f}%" if total_testes > 0 else "0%")
        
    elif opcao == "8":
        executar_todos_testes()
    elif opcao == "0":
        print("Saindo...")
        return False
    else:
        print("Opção inválida!")
    
    return True

def executar_todos_testes():
    """Executa todos os testes"""
    
    # Inicia relatório completo
    nome_arquivo_relatorio = iniciar_relatorio("Todos_Testes")
    
    classes_teste = [
        ("Testes de Login", TestesLogin),
        ("Testes de Cadastro de Responsável", TestesCadastroResponsavel),
        ("Testes de Listagem de Responsável", TestesListagemResponsavel),
        ("Testes de Cadastro de Bombona", TestesCadastroBombona),
        ("Testes de Listagem de Bombona", TestesListagemBombona),
        ("Testes de Integração", TestesIntegracao),
        ("Testes de Relatórios", TestesRelatorios)
    ]
    
    for nome_secao, classe_teste in classes_teste:
        escrever_relatorio(f"\n{'=' * 70}")
        escrever_relatorio(f"SEÇÃO: {nome_secao}")
        escrever_relatorio(f"{'=' * 70}")
        
        instancia = classe_teste()
        instancia.executar_todos_testes()
    
    # Fecha relatório
    fechar_relatorio()
    
    print(f"\nRelatório completo salvo em: {nome_arquivo_relatorio}")

# ==================== PONTO DE ENTRADA ====================

if __name__ == "__main__":
    # Verifica imagens necessárias
    imagens_necessarias = [
        "login_screen.png",
        "main_interface.png",
        "btn_cadastrar_responsavel.png",
        "btn_listar_responsaveis.png",
        "btn_cadastrar_bombona.png",
        "btn_listar_bombonas.png",
        "btn_relatorios.png",
        "btn_editar.png",
        "btn_excluir.png",
        "success_message.png",
        "error_message.png",
        "lista_responsaveis.png",
        "lista_bombonas.png",
        "table_header.png",
        "save_dialog.png",
        "dialog_box.png",
        "combo_formato.png",
        "opcao_csv.png",
        "opcao_pdf.png",
        "btn_relatorio_bombonas.png",
        "btn_relatorio_responsaveis.png"
    ]
    
    imagens_faltando = [img for img in imagens_necessarias if not (DIRETORIO_SCREENSHOTS / img).exists()]
    
    if imagens_faltando:
        print("ATENÇÃO: Imagens necessárias não encontradas:")
        for img in imagens_faltando:
            print(f"   - {DIRETORIO_SCREENSHOTS / img}")
        print("\nExecute a aplicação manualmente e capture estas telas.")
        print("Use: pyautogui.screenshot('caminho/para/imagem.png')")
        print("\nExecute este script novamente após capturar as imagens.")
        sys.exit(1)
    
    # Loop do menu
    continuar = True
    while continuar:
        opcao = exibir_menu()
        continuar = executar_opcao(opcao)
        
        if continuar:
            input("\nPressione ENTER para continuar...")
    
    print("\nTestes finalizados!")
texto("usuario_errado")
            pressionar_tecla("tab")
            digitar_texto("senha_errada")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar credenciais inválidas",
                sucesso,
                "Deveria ainda estar na tela de login" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_campos_vazios(self):
        """Deve rejeitar login com campos vazios"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Rejeitar login com campos vazios")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar login com campos vazios",
                sucesso,
                "Deveria mostrar erro e continuar na tela de login" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE CADASTRO DE RESPONSÁVEL ====================

class TestesCadastroResponsavel:
    """Testes de cadastro de responsáveis"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de cadastro"""
        self.testar_criar_responsavel_valido()
        self.testar_rejeitar_cpf_invalido()
        self.testar_rejeitar_cpf_tamanho_incorreto()
        self.testar_rejeitar_campos_vazios_responsavel()
    
    def testar_criar_responsavel_valido(self):
        """Deve criar um novo responsável com dados válidos"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Criar responsável válido")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_