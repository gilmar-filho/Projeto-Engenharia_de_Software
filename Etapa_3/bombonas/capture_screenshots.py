"""
Script simples para capturar screenshots necessários
Execute este arquivo DEPOIS de abrir sua aplicação
"""
import pyautogui
import time
from pathlib import Path

# Cria pasta se não existir
screenshots_dir = Path("tests/screenshots")
screenshots_dir.mkdir(parents=True, exist_ok=True)

def capture_with_delay(filename, delay=3):
    """Captura screenshot com delay"""
    print(f"\n📸 Capturando: {filename}")
    print(f"⏳ Você tem {delay} segundos para posicionar a tela...")
    
    for i in range(delay, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Captura a tela inteira (depois você pode recortar)
    screenshot = pyautogui.screenshot()
    filepath = screenshots_dir / filename
    screenshot.save(str(filepath))
    
    print(f"✅ Salvo: {filepath}")
    print(f"📏 Tamanho: {screenshot.size}")

def main():
    """Captura todas as imagens necessárias"""
    print("🚀 CAPTURADOR DE SCREENSHOTS")
    print("="*50)
    print("INSTRUÇÕES:")
    print("1. Abra sua aplicação")
    print("2. Para cada tela, posicione a janela")
    print("3. Aguarde a captura automática")
    print()
    
    input("📱 Aplicação está aberta? Pressione ENTER para continuar...")
    
    # Capturas necessárias
    captures = [
        ("login_screen.png", "Tela de LOGIN"),
        ("main_interface.png", "Interface PRINCIPAL (após login)"),
        ("btn_cadastrar_responsavel.png", "Tela com botão CADASTRAR RESPONSÁVEL visível"),
        ("success_message.png", "Mensagem de SUCESSO (cadastre algo para ver)")
    ]
    
    for filename, description in captures:
        print("\n" + "="*50)
        print(f"📋 PRÓXIMA CAPTURA: {description}")
        print(f"📄 Arquivo: {filename}")
        
        ready = input("✋ Tela posicionada? (ENTER=sim, s=pular): ")
        if ready.lower() == 's':
            print("⏭️ Pulando...")
            continue
            
        capture_with_delay(filename, delay=3)
    
    print("\n🎉 CAPTURAS CONCLUÍDAS!")
    print(f"📁 Pasta: {screenshots_dir.absolute()}")
    print("🧪 Agora execute: python tests/test_e2e.py")

if __name__ == "__main__":
    main()