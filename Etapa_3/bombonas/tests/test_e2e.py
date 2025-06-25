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
import pytest

# ==================== CONFIGURAÇÃO GLOBAL ====================

# Diretórios
PROJECT_DIR = Path(__file__).parent.parent
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"

# Cria pasta de screenshots se não existir
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True  # Move mouse para canto superior esquerdo para parar
pyautogui.PAUSE = 1.0  # Pausa de 1 segundo entre ações

# ==================== UTILITÁRIOS BÁSICOS ====================


def start_app():
    """
    Inicia a aplicação - equivale ao cy.visit() do Cypress

    Returns:
        subprocess.Popen: Processo da aplicação
    """
    print("🚀 Iniciando aplicação...")

    # Inicia a aplicação como subprocesso
    process = subprocess.Popen([sys.executable, str(PROJECT_DIR / "main.py")])

    # Aguarda a aplicação carregar
    time.sleep(4)  # Ajuste conforme necessário

    print("✅ Aplicação iniciada")
    return process


def stop_app(process):
    """
    Para a aplicação - equivale ao fechar navegador no Cypress

    Args:
        process: Processo da aplicação
    """
    print("🛑 Parando aplicação...")

    try:
        process.terminate()
        process.wait(timeout=5)  # Aguarda 5 segundos
    except subprocess.TimeoutExpired:
        print("⚠️ Forçando encerramento...")
        process.kill()

    time.sleep(1)
    print("✅ Aplicação parada")


def click_image(image_name, confidence=0.8, timeout=5):
    """
    Clica em uma imagem na tela - equivale ao cy.get().click()

    Args:
        image_name (str): Nome do arquivo de imagem
        confidence (float): Confiança do reconhecimento (0.0 a 1.0)
        timeout (int): Tempo limite para encontrar a imagem

    Returns:
        bool: True se clicou com sucesso, False caso contrário
    """
    image_path = SCREENSHOTS_DIR / image_name

    if not image_path.exists():
        print(f"❌ Imagem não encontrada: {image_path}")
        return False

    print(f"🔍 Procurando por: {image_name}")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                print(f"✅ Clicou em: {image_name}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"⚠️ Erro ao procurar imagem: {e}")

        time.sleep(0.5)

    print(f"❌ Imagem não encontrada após {timeout}s: {image_name}")
    return False


def type_text(text, interval=0.1):
    """
    Digita texto - equivale ao cy.type() do Cypress

    Args:
        text (str): Texto a ser digitado
        interval (float): Intervalo entre caracteres
    """
    print(f"⌨️ Digitando: {text}")
    pyautogui.write(text, interval=interval)


def press_key(key):
    """
    Pressiona uma tecla - equivale ao cy.type('{key}') do Cypress

    Args:
        key (str): Nome da tecla (enter, tab, escape, etc.)
    """
    print(f"🔘 Pressionando: {key}")
    pyautogui.press(key)


def wait_for_image(image_name, timeout=10, confidence=0.8):
    """
    Aguarda uma imagem aparecer na tela - equivale ao cy.wait() do Cypress

    Args:
        image_name (str): Nome do arquivo de imagem
        timeout (int): Tempo limite em segundos
        confidence (float): Confiança do reconhecimento

    Returns:
        bool: True se encontrou a imagem, False se timeout
    """
    image_path = SCREENSHOTS_DIR / image_name

    if not image_path.exists():
        print(f"❌ Imagem não encontrada: {image_path}")
        return False

    print(f"⏳ Aguardando: {image_name} (timeout: {timeout}s)")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
            if location:
                print(f"✅ Imagem encontrada: {image_name}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"⚠️ Erro ao aguardar imagem: {e}")

        time.sleep(0.5)

    print(f"❌ Timeout aguardando: {image_name}")
    return False


def should_see_image(image_name, confidence=0.8):
    """
    Verifica se uma imagem está visível - equivale ao cy.should('be.visible')

    Args:
        image_name (str): Nome do arquivo de imagem
        confidence (float): Confiança do reconhecimento

    Returns:
        bool: True se imagem está visível, False caso contrário
    """
    image_path = SCREENSHOTS_DIR / image_name

    if not image_path.exists():
        print(f"❌ Imagem não encontrada: {image_path}")
        return False

    try:
        location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
        visible = location is not None

        if visible:
            print(f"✅ Imagem visível: {image_name}")
        else:
            print(f"❌ Imagem não visível: {image_name}")

        return visible
    except Exception as e:
        print(f"⚠️ Erro ao verificar imagem: {e}")
        return False


def do_login():
    """
    Realiza login padrão - função helper reutilizável

    Returns:
        bool: True se login foi bem-sucedido
    """
    print("🔐 Realizando login...")

    # Aguarda tela de login
    if not wait_for_image("login_screen.png", timeout=10):
        return False

    # Digita credenciais
    type_text("admin")
    press_key("tab")
    type_text("123456")
    press_key("enter")

    # Aguarda interface principal
    return wait_for_image("main_interface.png", timeout=10)


def close_any_dialogs():
    """
    Fecha diálogos que possam estar abertos
    """
    print("🗂️ Fechando possíveis diálogos...")
    press_key("enter")  # Fecha mensagem de sucesso
    time.sleep(0.5)
    press_key("escape")  # Volta para tela principal
    time.sleep(0.5)


# ==================== TESTES E2E ====================


class TestLoginFlow:
    """Testes do fluxo de login - equivale a describe('Login') no Cypress"""

    def test_should_display_login_screen(self):
        """Deve exibir a tela de login ao iniciar a aplicação"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Exibir tela de login")
        print("=" * 60)

        app = start_app()

        try:
            # Verifica se tela de login está visível
            assert wait_for_image(
                "login_screen.png", timeout=10
            ), "Tela de login não apareceu"

            print("✅ PASSOU: Tela de login exibida corretamente")

        finally:
            stop_app(app)

    def test_should_login_with_valid_credentials(self):
        """Deve fazer login com credenciais válidas"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Login com credenciais válidas")
        print("=" * 60)

        app = start_app()

        try:
            # Realiza login
            assert do_login(), "Login não foi realizado com sucesso"

            print("✅ PASSOU: Login realizado com sucesso")

        finally:
            stop_app(app)

    def test_should_reject_invalid_credentials(self):
        """Deve rejeitar credenciais inválidas"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Rejeitar credenciais inválidas")
        print("=" * 60)

        app = start_app()

        try:
            # Aguarda tela de login
            assert wait_for_image("login_screen.png"), "Tela de login não apareceu"

            # Digita credenciais inválidas
            type_text("wrong")
            press_key("tab")
            type_text("wrong")
            press_key("enter")

            time.sleep(2)

            # Verifica se ainda está na tela de login (não logou)
            assert should_see_image(
                "login_screen.png"
            ), "Deveria ainda estar na tela de login"

            print("✅ PASSOU: Credenciais inválidas rejeitadas")

        finally:
            stop_app(app)


class TestResponsavelCRUD:
    """Testes CRUD de responsáveis - equivale a describe('Responsavel') no Cypress"""

    def test_should_create_new_responsavel(self):
        """Deve criar um novo responsável"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Criar novo responsável")
        print("=" * 60)

        app = start_app()

        try:
            # Login
            assert do_login(), "Erro no login"

            # Clica em "Cadastrar Responsável"
            assert click_image(
                "btn_cadastrar_responsavel.png"
            ), "Botão 'Cadastrar Responsável' não encontrado"

            time.sleep(1)

            # Preenche formulário
            type_text("83249657000")  # CPF
            press_key("tab")
            type_text("Joao Silva")  # Nome
            press_key("tab")
            type_text("11999887766")  # Telefone
            press_key("tab")
            type_text("LABORATORIO")  # Setor

            # Submete formulário
            press_key("enter")
            time.sleep(2)

            # Verifica mensagem de sucesso
            assert should_see_image(
                "success_message.png"
            ), "Mensagem de sucesso não apareceu"

            print("✅ PASSOU: Responsável criado com sucesso")

        finally:
            stop_app(app)

    def test_should_list_responsaveis(self):
        """Deve listar responsáveis cadastrados"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Listar responsáveis")
        print("=" * 60)

        app = start_app()

        try:
            # Login
            assert do_login(), "Erro no login"

            # Clica em "Listar Responsáveis"
            assert click_image(
                "btn_listar_responsaveis.png"
            ), "Botão 'Listar Responsáveis' não encontrado"

            time.sleep(2)

            # Verifica se lista apareceu
            assert should_see_image(
                "lista_responsaveis.png"
            ), "Lista de responsáveis não apareceu"

            print("✅ PASSOU: Lista de responsáveis exibida")

        finally:
            stop_app(app)


class TestBombonaCRUD:
    """Testes CRUD de bombonas - equivale a describe('Bombona') no Cypress"""

    def test_should_create_new_bombona(self):
        """Deve criar uma nova bombona"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Criar nova bombona")
        print("=" * 60)

        app = start_app()

        try:
            # Login
            assert do_login(), "Erro no login"

            # # Primeiro cadastra um responsável (pré-requisito)
            # print("📋 Cadastrando responsável pré-requisito...")
            # assert click_image(
            #     "btn_cadastrar_responsavel.png"
            # ), "Botão 'Cadastrar Responsável' não encontrado"

            # time.sleep(1)
            # type_text("85476994068")
            # press_key("tab")
            # type_text("Roberto Martins")
            # press_key("tab")
            # type_text("11995678324")
            # press_key("tab")
            # type_text("TECNOLOGIA")
            # press_key("enter")
            # time.sleep(2)

            # # Fecha dialogs e volta para principal
            # # close_any_dialogs()
            # press_key("enter")  # Fecha mensagem de sucesso
            # time.sleep(0.5)
            # press_key("tab")    # Seleciona o botão 'não'
            # time.sleep(0.5)
            # press_key("enter")  # Recusa a criação de novo Responsável
            # time.sleep(0.5)

            # time.sleep(1)

            # Agora cadastra a bombona
            print("🧪 Cadastrando bombona...")
            assert click_image(
                "btn_cadastrar_bombona.png"
            ), "Botão 'Cadastrar Bombona' não encontrado"

            time.sleep(1)

            # Preenche dados da bombona
            type_text("LAB-001")  # Código
            press_key("tab")
            type_text("25.5")  # Volume
            press_key("tab")
            press_key("down")  # Seleciona tipo resíduo
            press_key("tab")
            press_key("down")  # Seleciona responsável
            press_key("tab")

            # Submete
            press_key("enter")
            time.sleep(2)

            # Verifica sucesso
            assert should_see_image(
                "success_message.png"
            ), "Bombona não foi cadastrada com sucesso"

            print("✅ PASSOU: Bombona criada com sucesso")

        finally:
            stop_app(app)


class TestNavigationFlow:
    """Testes de navegação - equivale a describe('Navigation') no Cypress"""

    def test_should_navigate_between_screens(self):
        """Deve navegar entre as telas do sistema"""
        print("\n" + "=" * 60)
        print("🧪 TESTE: Navegação entre telas")
        print("=" * 60)

        app = start_app()

        try:
            # Login
            assert do_login(), "Erro no login"

            # Testa navegação para cada tela principal
            screens_to_test = [
                "btn_cadastrar_responsavel.png",
                "btn_listar_responsaveis.png",
                "btn_cadastrar_bombona.png",
                "btn_listar_bombonas.png",
            ]

            for screen_button in screens_to_test:
                print(f"🔗 Testando navegação: {screen_button}")

                # Clica no botão
                if click_image(screen_button):
                    time.sleep(1)
                    # Volta para tela principal
                    press_key("escape")
                    time.sleep(1)
                    print(f"✅ Navegação OK: {screen_button}")
                else:
                    print(f"⚠️ Botão não encontrado: {screen_button}")

            print("✅ PASSOU: Navegação entre telas funcionando")

        finally:
            stop_app(app)


# ==================== RUNNER PRINCIPAL ====================


def run_all_tests():
    """
    Executa todos os testes - equivale ao 'npx cypress run'
    """
    print("\n" + "🚀" + " INICIANDO TESTES E2E ".center(58, "=") + "🚀")
    print("Sistema de Gerenciamento de Bombonas")
    print("Simulando comportamento do Cypress para Tkinter")
    print("=" * 60)

    # Lista de classes de teste
    test_classes = [
        TestLoginFlow(),
        TestResponsavelCRUD(),
        TestBombonaCRUD(),
        TestNavigationFlow(),
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    # Executa cada classe de teste
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"\n📂 EXECUTANDO: {class_name}")
        print("-" * 60)

        # Pega todos os métodos que começam com 'test_'
        test_methods = [
            method for method in dir(test_class) if method.startswith("test_")
        ]

        for test_method_name in test_methods:
            total_tests += 1
            test_method = getattr(test_class, test_method_name)

            try:
                test_method()
                passed_tests += 1

            except Exception as e:
                failed_tests += 1
                print(f"\n❌ FALHOU: {class_name}.{test_method_name}")
                print(f"   Erro: {str(e)}")

            print("-" * 30)

    # Relatório final
    print("\n" + "📊" + " RELATÓRIO FINAL ".center(58, "=") + "📊")
    print(f"✅ Testes passaram: {passed_tests}")
    print(f"❌ Testes falharam: {failed_tests}")
    print(f"📈 Total executado: {total_tests}")

    if failed_tests == 0:
        print("🎉 TODOS OS TESTES PASSARAM! 🎉")
    else:
        print(f"⚠️ {failed_tests} teste(s) falharam")

    print("=" * 60)

    return failed_tests == 0


# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    # Verifica se pasta de screenshots existe
    if not SCREENSHOTS_DIR.exists():
        print("📁 Criando pasta de screenshots...")
        SCREENSHOTS_DIR.mkdir()

    # Lista imagens necessárias
    required_images = [
        "login_screen.png",
        "main_interface.png",
        "btn_cadastrar_responsavel.png",
        "btn_listar_responsaveis.png",
        "btn_cadastrar_bombona.png",
        "btn_listar_bombonas.png",
        "success_message.png",
        "lista_responsaveis.png",
    ]

    missing_images = [
        img for img in required_images if not (SCREENSHOTS_DIR / img).exists()
    ]

    if missing_images:
        print("⚠️ ATENÇÃO: Imagens necessárias não encontradas:")
        for img in missing_images:
            print(f"   - {SCREENSHOTS_DIR / img}")
        print("\n📸 Execute a aplicação manualmente e capture estas telas.")
        print("💡 Use: pyautogui.screenshot('caminho/para/imagem.png')")
        print("\n🔄 Execute este script novamente após capturar as imagens.")
    else:
        # Executa os testes
        success = run_all_tests()

        # Exit code para integração com CI/CD
        sys.exit(0 if success else 1)
