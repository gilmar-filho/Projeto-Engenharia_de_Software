"""
Módulo base para testes E2E
Contém todas as funções utilitárias compartilhadas entre os módulos de teste
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
DIRETORIO_PROJETO = Path(__file__).parent.parent.parent
DIRETORIO_SCREENSHOTS = Path(__file__).parent.parent / "screenshots"
DIRETORIO_RELATORIOS = Path(__file__).parent.parent / "relatorios"

# Cria pastas se não existirem
DIRETORIO_SCREENSHOTS.mkdir(exist_ok=True)
DIRETORIO_RELATORIOS.mkdir(exist_ok=True)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True  
pyautogui.PAUSE = 1.0  

# Variáveis globais para relatório
arquivo_relatorio = None
total_testes = 0
testes_passaram = 0
testes_falharam = 0

# ==================== FUNÇÕES DE RELATÓRIO ====================

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
    escrever_relatorio("RELATORIO DE TESTES E2E - SISTEMA DE BOMBONAS")
    if nome_secao:
        escrever_relatorio(f"Secao: {nome_secao}")
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

def obter_estatisticas():
    """Retorna as estatísticas atuais dos testes"""
    global total_testes, testes_passaram, testes_falharam
    return {
        'total': total_testes,
        'passaram': testes_passaram,
        'falharam': testes_falharam,
        'taxa_sucesso': (testes_passaram/total_testes*100) if total_testes > 0 else 0
    }

# ==================== FUNÇÕES DE CONTROLE DA APLICAÇÃO ====================

def iniciar_aplicacao():
    """Inicia a aplicação"""
    escrever_relatorio("Iniciando aplicacao...")
    
    processo = subprocess.Popen([sys.executable, str(DIRETORIO_PROJETO / "main.py")])
    time.sleep(4)
    
    escrever_relatorio("Aplicacao iniciada")
    return processo

def parar_aplicacao(processo):
    """Para a aplicação"""
    escrever_relatorio("Parando aplicacao...")
    
    try:
        processo.terminate()
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        escrever_relatorio("Forcando encerramento...")
        processo.kill()
    
    time.sleep(1)
    escrever_relatorio("Aplicacao parada")

# ==================== FUNÇÕES DE INTERAÇÃO COM INTERFACE ====================

def clicar_imagem(nome_imagem, confianca=0.8, timeout=5):
    """Clica em uma imagem na tela"""
    caminho_imagem = DIRETORIO_SCREENSHOTS / nome_imagem
    
    if not caminho_imagem.exists():
        escrever_relatorio(f"Imagem nao encontrada: {caminho_imagem}")
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
    
    escrever_relatorio(f"Imagem nao encontrada apos {timeout}s: {nome_imagem}")
    return False

def aguardar_imagem(nome_imagem, timeout=10, confianca=0.8):
    """Aguarda uma imagem aparecer na tela"""
    caminho_imagem = DIRETORIO_SCREENSHOTS / nome_imagem
    
    if not caminho_imagem.exists():
        escrever_relatorio(f"Imagem nao encontrada: {caminho_imagem}")
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
        escrever_relatorio(f"Imagem nao encontrada: {caminho_imagem}")
        return False
    
    try:
        localizacao = pyautogui.locateOnScreen(str(caminho_imagem), confidence=confianca)
        visivel = localizacao is not None
        
        if visivel:
            escrever_relatorio(f"Imagem visivel: {nome_imagem}")
        else:
            escrever_relatorio(f"Imagem nao visivel: {nome_imagem}")
        
        return visivel
    except Exception as e:
        escrever_relatorio(f"Erro ao verificar imagem: {e}")
        return False

# ==================== FUNÇÕES DE ENTRADA DE DADOS ====================

def digitar_texto(texto, intervalo=0.1):
    """Digita texto"""
    escrever_relatorio(f"Digitando: {texto}")
    pyautogui.write(texto, interval=intervalo)

def pressionar_tecla(tecla):
    """Pressiona uma tecla"""
    escrever_relatorio(f"Pressionando: {tecla}")
    pyautogui.press(tecla)

def selecionar_item_aleatorio_lista():
    """Seleciona um item aleatório da lista usando as setas"""
    escrever_relatorio("Selecionando item aleatorio da lista...")
    
    # Número aleatório de setas para baixo (entre 0 e 4)
    quantidade_setas = random.randint(0, 4)
    
    for i in range(quantidade_setas):
        pressionar_tecla("down")
        time.sleep(0.2)
    
    # Pressiona espaço para selecionar
    pressionar_tecla("space")
    time.sleep(0.5)
    
    return True

def limpar_campos_formulario(quantidade_tabs):
    """Limpa campos do formulário usando Ctrl+A e Delete"""
    for i in range(quantidade_tabs):
        pyautogui.hotkey('ctrl', 'a')
        pressionar_tecla('delete')
        pressionar_tecla('tab')

# ==================== FUNÇÕES AUXILIARES ====================

def fazer_login(usuario="admin", senha="123456"):
    """Realiza login"""
    escrever_relatorio(f"Realizando login com usuario: {usuario}")
    
    if not aguardar_imagem("login_screen.png", timeout=10):
        return False
    
    digitar_texto(usuario)
    pressionar_tecla("tab")
    digitar_texto(senha)
    pressionar_tecla("enter")
    
    return aguardar_imagem("main_interface.png", timeout=10)

def fechar_dialogos():
    """Fecha diálogos que possam estar abertos"""
    escrever_relatorio("Fechando possiveis dialogos...")
    
    # Primeiro tenta com ESC (fecha sem confirmar)
    pressionar_tecla("escape")
    time.sleep(0.5)
    
    # Se ainda houver diálogo, usa Tab + Enter para selecionar "Não"
    if verificar_imagem_visivel("dialog_box.png", confianca=0.7):
        pressionar_tecla("tab")
        time.sleep(0.2)
        pressionar_tecla("enter")
        time.sleep(0.5)

# ==================== VALIDAÇÃO DE IMAGENS ====================

def verificar_imagens_necessarias():
    """Verifica se todas as imagens necessárias estão disponíveis"""
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
    
    imagens_faltando = []
    for img in imagens_necessarias:
        if not (DIRETORIO_SCREENSHOTS / img).exists():
            imagens_faltando.append(img)
    
    return imagens_faltando

# ==================== CLASSE BASE PARA TESTES ====================

class TesteBase:
    """Classe base para todos os testes"""
    
    def __init__(self):
        self.nome_classe = self.__class__.__name__
    
    def executar_todos_testes(self):
        """Método a ser sobrescrito pelas classes filhas"""
        raise NotImplementedError("Este método deve ser implementado pela classe filha")
    
    def iniciar_teste(self, nome_teste):
        """Inicia um teste específico"""
        escrever_relatorio("\n" + "=" * 60)
        escrever_relatorio(f"TESTE: {nome_teste}")
        escrever_relatorio("=" * 60)