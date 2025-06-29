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

def iniciar_relatorio():
    """Inicia o arquivo de relatório de testes"""
    global arquivo_relatorio
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = DIRETORIO_RELATORIOS / f"relatorio_testes_{timestamp}.txt"
    
    arquivo_relatorio = open(nome_arquivo, 'w', encoding='utf-8')
    
    escrever_relatorio("=" * 70)
    escrever_relatorio("RELATÓRIO DE TESTES E2E - SISTEMA DE BOMBONAS")
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
    pressionar_tecla("enter")
    time.sleep(0.5)
    pressionar_tecla("escape")
    time.sleep(0.5)

def limpar_campos_formulario(quantidade_tabs):
    """Limpa campos do formulário usando Ctrl+A e Delete"""
    for i in range(quantidade_tabs):
        pyautogui.hotkey('ctrl', 'a')
        pressionar_tecla('delete')
        pressionar_tecla('tab')

def navegar_e_selecionar_item_lista(posicao='primeiro', acao=None):
    """
    Clica no centro da tela para focar a lista, navega para um item e, 
    opcionalmente, clica em um botão de ação.
    """
    escrever_relatorio("Focando na lista ao clicar no centro da tela...")
    largura, altura = pyautogui.size()
    pyautogui.click(largura / 2, altura / 2)  # Clica no centro da tela para garantir o foco
    time.sleep(0.5)

    if posicao == 'primeiro':
        escrever_relatorio("Selecionando o primeiro item da lista (pressionando 'up')...")
        for i in range(10) :
            pressionar_tecla('up')
    elif posicao == 'ultimo':
        escrever_relatorio("Selecionando o último item da lista (pressionando 'down')...")
        for i in range(10) :
            pressionar_tecla('down')
    
    time.sleep(0.5)

    if acao:
        nome_botao = f"btn_{acao}.png"
        escrever_relatorio(f"Tentando clicar no botão de '{acao}'...")
        if not clicar_imagem(nome_botao, timeout=5):
            registrar_teste(f"Ação '{acao}' na lista", False, f"Botão '{nome_botao}' não encontrado.")
            return False
    
    return True

# ==================== TESTES DE LOGIN ====================

class TestesLogin:
    """Testes do fluxo de login"""
    
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
            
            digitar_texto("usuario_errado")
            pressionar_tecla("tab")
            digitar_texto("senha_errada")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve mostrar mensagem de erro e continuar na tela de login
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
            
            # Tenta fazer login sem preencher nada
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar login com campos vazios",
                sucesso,
                "Deveria mostrar erro e continuar na tela de login" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE RESPONSÁVEL ====================

class TestesResponsavel:
    """Testes CRUD de responsáveis"""
    
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
            
            # Dados válidos
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
            
            # CPF com todos dígitos iguais
            digitar_texto("11111111111")
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
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
            
            # CPF com menos de 11 dígitos
            digitar_texto("123456789")
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
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
            
            # Tenta cadastrar sem preencher nada
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro com campos vazios",
                sucesso,
                "Deveria rejeitar cadastro sem dados" if not sucesso else ""
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
            
            # Primeiro cria um responsável
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("37499187080")
            pressionar_tecla("tab")
            digitar_texto("Maria Santos Original")
            pressionar_tecla("tab")
            digitar_texto("11988776655")
            pressionar_tecla("tab")
            digitar_texto("FINANCEIRO")
            
            pressionar_tecla("enter")
            pressionar_tecla("enter")

            time.sleep(2)
            fechar_dialogos()
            
            # Agora lista e edita
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Navega na lista e edita
            if navegar_e_selecionar_item_lista(posicao='ultimo', acao='editar'):
                time.sleep(1)
                
                # Limpa e edita o nome
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
                    "Não conseguiu selecionar o item ou clicar no botão de edição."
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
            
            # Cria um responsável para remover
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("50572033044")
            pressionar_tecla("tab")
            digitar_texto("Teste Remocao")
            pressionar_tecla("tab")
            digitar_texto("11977665544")
            pressionar_tecla("tab")
            digitar_texto("TEMPORARIO")
            pressionar_tecla("enter")
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Lista e remove
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Navega na lista e exclui
            if navegar_e_selecionar_item_lista(posicao='ultimo', acao='excluir'):
                time.sleep(1)
                
                # Confirma exclusão (geralmente um pop-up de confirmação)
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
                    "Não conseguiu selecionar o item ou clicar no botão de exclusão."
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE BOMBONA ====================

class TestesBombona:
    """Testes CRUD de bombonas"""
    
    def testar_criar_bombona_valida(self):
        """Deve criar uma nova bombona com dados válidos"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Criar bombona válida")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Primeiro cria um responsável
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("17076053004")
            pressionar_tecla("tab")
            digitar_texto("Responsavel Bombona")
            pressionar_tecla("tab")
            digitar_texto("11966554433")
            pressionar_tecla("tab")
            digitar_texto("QUIMICA")
            pressionar_tecla("enter")
            
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Agora cria a bombona
            clicar_imagem("btn_cadastrar_bombona.png")
            time.sleep(1)
            
            digitar_texto("LAB-001")
            pressionar_tecla("tab")
            digitar_texto("50.5")
            pressionar_tecla("tab")
            pressionar_tecla("down")  # Seleciona tipo
            pressionar_tecla("tab")
            
            # Seleciona o responsável criado (último da lista)
            for i in range(10):
                pressionar_tecla("down")
            pressionar_tecla("enter")
            
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
            
            # Código inválido (não segue padrão LLL-NNN)
            digitar_texto("12345")
            pressionar_tecla("tab")
            digitar_texto("30")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            pressionar_tecla("tab")
            pressionar_tecla("down")
            pressionar_tecla("enter")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
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
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
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
            
            # Tenta cadastrar sem preencher nada
            pressionar_tecla("enter")
            time.sleep(2)
            
            # Deve mostrar erro
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro de bombona sem dados",
                sucesso,
                "Deveria rejeitar cadastro sem preencher campos" if not sucesso else ""
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
            
            # Navega na lista e edita
            if navegar_e_selecionar_item_lista(posicao='ultimo', acao='editar'):
                time.sleep(1)
                
                # Edita o volume
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
                    "Não conseguiu selecionar a bombona para editar."
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
            
            # Navega na lista e exclui
            if navegar_e_selecionar_item_lista(posicao='ultimo', acao='excluir'):
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
                    "Não conseguiu selecionar a bombona para remover."
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE INTEGRAÇÃO ====================

class TestesIntegracao:
    """Testes de integração entre módulos"""
    
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
            
            digitar_texto("29286344015")
            pressionar_tecla("tab")
            digitar_texto("Responsavel Com Bombona")
            pressionar_tecla("tab")
            digitar_texto("11955443322")
            pressionar_tecla("tab")
            digitar_texto("PRODUCAO")
            
            pressionar_tecla("enter")
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
            
            # Seleciona o responsável criado (último da lista)
            for i in range(10):
                pressionar_tecla("down")
            
            pressionar_tecla("enter")
            pressionar_tecla("enter")
            pressionar_tecla("enter")
            time.sleep(2)
            fechar_dialogos()
            
            # Tenta remover o responsável
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # ALTERAÇÃO AQUI: Usa 'up' para selecionar o último item adicionado
            if navegar_e_selecionar_item_lista(posicao='ultimo', acao='excluir'):
                time.sleep(1)
                pressionar_tecla("enter") # Confirma a tentativa de exclusão
                time.sleep(2)
                
                # Deve mostrar erro, não sucesso
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
                    "Não encontrou ou não conseguiu clicar no botão de exclusão para o responsável."
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
            
            # Navega e edita
            if navegar_e_selecionar_item_lista(posicao='primeiro', acao='editar'):
                time.sleep(1)
                
                # Tenta deixar o nome vazio
                pyautogui.hotkey('ctrl', 'a')
                pressionar_tecla('delete')
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                # Deve mostrar erro
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
                    "Não encontrou item para editar"
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
            
            # Navega e edita
            if navegar_e_selecionar_item_lista(posicao='primeiro', acao='editar'):
                time.sleep(1)
                
                # Tenta colocar volume negativo
                pyautogui.hotkey('ctrl', 'a')
                digitar_texto("-50")
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                # Deve mostrar erro
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
                    "Não encontrou bombona para editar"
                )
            
        finally:
            parar_aplicacao(app)

# ==================== TESTES DE NAVEGAÇÃO ====================

class TestesNavegacao:
    """Testes de navegação e interface"""
    
    def testar_navegacao_entre_telas(self):
        """Deve navegar entre as telas do sistema"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio("TESTE: Navegação entre telas")
        escrever_relatorio("=" * 60)
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            telas_para_testar = [
                ("btn_cadastrar_responsavel.png", "Cadastrar Responsável"),
                ("btn_listar_responsaveis.png", "Listar Responsáveis"),
                ("btn_cadastrar_bombona.png", "Cadastrar Bombona"),
                ("btn_listar_bombonas.png", "Listar Bombonas"),
                ("btn_relatorios.png", "Relatórios")
            ]
            
            for botao, nome_tela in telas_para_testar:
                escrever_relatorio(f"Testando navegação: {nome_tela}")
                
                if clicar_imagem(botao):
                    time.sleep(1)
                    if nome_tela == "Listar Responsáveis" or nome_tela == "Listar Bombonas":
                        clicar_imagem("btn_fechar.png")
                    else:    
                        pressionar_tecla("escape")
                    time.sleep(1)
                    registrar_teste(f"Navegação para {nome_tela}", True)
                else:
                    registrar_teste(f"Navegação para {nome_tela}", False, "Botão não encontrado")
            
        finally:
            parar_aplicacao(app)
    
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
                clicar_imagem("combo_formato.png", confianca=0.7)
                time.sleep(0.5)
                pressionar_tecla("enter")
                
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

# ==================== EXECUÇÃO DOS TESTES ====================

def resetar_contadores_globais():
    """Reseta os contadores de resultado dos testes."""
    global total_testes, testes_passaram, testes_falharam
    total_testes = 0
    testes_passaram = 0
    testes_falharam = 0

def executar_suites_de_teste(classes_de_teste_instanciadas):
    """Executa uma lista de suítes de teste e gera relatório"""
    
    # Garante que os contadores estão zerados para esta execução
    resetar_contadores_globais()
    
    # Inicia relatório
    nome_arquivo_relatorio = iniciar_relatorio()
    
    # Executa cada classe de teste
    for classe_teste in classes_de_teste_instanciadas:
        nome_classe = classe_teste.__class__.__name__
        escrever_relatorio(f"\n{'=' * 70}")
        escrever_relatorio(f"EXECUTANDO CLASSE: {nome_classe}")
        escrever_relatorio(f"{'=' * 70}")
        
        # Pega todos os métodos que começam com 'testar_'
        metodos_teste = [metodo for metodo in dir(classe_teste) if metodo.startswith("testar_")]
        
        for nome_metodo in metodos_teste:
            metodo_teste = getattr(classe_teste, nome_metodo)
            
            try:
                metodo_teste()
            except Exception as e:
                escrever_relatorio(f"\nERRO CRÍTICO: {nome_classe}.{nome_metodo}")
                escrever_relatorio(f"Exceção: {str(e)}")
                registrar_teste(nome_metodo, False, f"Erro crítico: {str(e)}")
            
            escrever_relatorio("-" * 30)
    
    # Fecha relatório
    fechar_relatorio()
    
    # Retorna informações sobre o relatório
    sucesso_geral = testes_passaram == total_testes if total_testes > 0 else True
    return nome_arquivo_relatorio, sucesso_geral

# ==================== PONTO DE ENTRADA ====================

if __name__ == "__main__":
    # Verifica se pasta de screenshots existe (lógica original mantida)
    if not DIRETORIO_SCREENSHOTS.exists():
        print(f"Criando pasta de screenshots em: {DIRETORIO_SCREENSHOTS}")
        DIRETORIO_SCREENSHOTS.mkdir()
    
    # Lista imagens necessárias (lógica original mantida)
    imagens_necessarias = [
        "login_screen.png", "main_interface.png", "btn_cadastrar_responsavel.png",
        "btn_listar_responsaveis.png", "btn_cadastrar_bombona.png", "btn_listar_bombonas.png",
        "btn_relatorios.png", "success_message.png", "error_message.png",
        "first_list_item.png", "last_list_item.png", "save_dialog.png",
        "combo_formato.png", "opcao_csv.png", "btn_relatorio_bombonas.png"
    ]
    
    imagens_faltando = [img for img in imagens_necessarias if not (DIRETORIO_SCREENSHOTS / img).exists()]
    
    if imagens_faltando:
        print("ATENÇÃO: Imagens necessárias não encontradas:")
        for img in imagens_faltando:
            print(f"   - {DIRETORIO_SCREENSHOTS / img}")
        print("\nExecute a aplicação manualmente e capture estas telas.")
        print("\nExecute este script novamente após capturar as imagens.")
        sys.exit(1) # Sai se as imagens não existirem

    # Dicionário mapeando opções do menu para as classes de teste
    suites_disponiveis = {
        '1': ("Testes de Login", [TestesLogin()]),
        '2': ("Testes de Responsável", [TestesResponsavel()]),
        '3': ("Testes de Bombona", [TestesBombona()]),
        '4': ("Testes de Integração", [TestesIntegracao()]),
        '5': ("Testes de Navegação", [TestesNavegacao()]),
    }

    # Lista com todas as suítes para a opção "Executar Todos"
    todas_as_suites = [
        TestesLogin(), TestesResponsavel(), TestesBombona(), 
        TestesIntegracao(), TestesNavegacao()
    ]
    
    # MODO INTERATIVO (com menu)
    while True:
        print("\n" + "="*40)
        print("   MENU DE EXECUÇÃO DE TESTES E2E")
        print("="*40)
        for key, (nome, _) in suites_disponiveis.items():
            print(f"  {key} - {nome}")
        print("-" * 40)
        print("  6 - EXECUTAR TODOS OS TESTES")
        print("  0 - Sair")
        print("="*40)
        
        escolha = input("Digite o número da suíte de testes que deseja executar: ")

        if escolha == '0':
            print("Saindo do script de testes.")
            break
        elif escolha == '6':
            print("\nExecutando TODAS as suítes de teste...")
            arquivo_rel, sucesso = executar_suites_de_teste(todas_as_suites)
            print(f"\nExecução concluída. Relatório salvo em: {arquivo_rel}")
            input("Pressione Enter para voltar ao menu...")
        elif escolha in suites_disponiveis:
            nome_suite, suite_para_executar = suites_disponiveis[escolha]
            print(f"\nExecutando: {nome_suite}...")
            arquivo_rel, sucesso = executar_suites_de_teste(suite_para_executar)
            print(f"\nExecução concluída. Relatório salvo em: {arquivo_rel}")
            input("Pressione Enter para voltar ao menu...")
        else:
            print("\nOpção inválida! Por favor, escolha um número do menu.")
            time.sleep(2)
