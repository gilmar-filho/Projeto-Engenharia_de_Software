"""
Módulo de testes de login
Testa todas as funcionalidades relacionadas ao login do sistema
"""

import time
from base_teste import *

class TestesLogin(TesteBase):
    """Testes do fluxo de login"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de login"""
        self.testar_exibir_tela_login()
        self.testar_login_credenciais_validas()
        self.testar_rejeitar_credenciais_invalidas()
        self.testar_login_campos_vazios()
        self.testar_login_apenas_usuario_preenchido()
        self.testar_login_apenas_senha_preenchida()
        self.testar_login_usuario_correto_senha_incorreta()
        self.testar_login_usuario_incorreto_senha_correta()
        self.testar_multiplas_tentativas_login()
    
    def testar_exibir_tela_login(self):
        """Deve exibir a tela de login ao iniciar a aplicação"""
        self.iniciar_teste("Exibir tela de login")
        
        app = iniciar_aplicacao()
        
        try:
            sucesso = aguardar_imagem("login_screen.png", timeout=10)
            registrar_teste(
                "Exibir tela de login",
                sucesso,
                "Tela de login nao apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_credenciais_validas(self):
        """Deve fazer login com credenciais válidas"""
        self.iniciar_teste("Login com credenciais validas")
        
        app = iniciar_aplicacao()
        
        try:
            sucesso = fazer_login()
            registrar_teste(
                "Login com credenciais validas",
                sucesso,
                "Login nao foi realizado com sucesso" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_credenciais_invalidas(self):
        """Deve rejeitar credenciais inválidas"""
        self.iniciar_teste("Rejeitar credenciais invalidas")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            digitar_texto("usuario_errado")
            pressionar_tecla("tab")
            digitar_texto("senha_errada")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar credenciais invalidas",
                sucesso,
                "Deveria ainda estar na tela de login" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_campos_vazios(self):
        """Deve rejeitar login com campos vazios"""
        self.iniciar_teste("Rejeitar login com campos vazios")
        
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
    
    def testar_login_apenas_usuario_preenchido(self):
        """Deve rejeitar login com apenas usuário preenchido"""
        self.iniciar_teste("Rejeitar login apenas com usuario")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            digitar_texto("admin")
            pressionar_tecla("tab")
            # Não digita senha
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar login apenas com usuario",
                sucesso,
                "Deveria rejeitar login sem senha" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_apenas_senha_preenchida(self):
        """Deve rejeitar login com apenas senha preenchida"""
        self.iniciar_teste("Rejeitar login apenas com senha")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            # Não digita usuário
            pressionar_tecla("tab")
            digitar_texto("123456")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar login apenas com senha",
                sucesso,
                "Deveria rejeitar login sem usuario" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_usuario_correto_senha_incorreta(self):
        """Deve rejeitar login com usuário correto e senha incorreta"""
        self.iniciar_teste("Rejeitar usuario correto com senha incorreta")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            digitar_texto("admin")
            pressionar_tecla("tab")
            digitar_texto("senha_errada")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar usuario correto com senha incorreta",
                sucesso,
                "Deveria rejeitar senha incorreta" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_login_usuario_incorreto_senha_correta(self):
        """Deve rejeitar login com usuário incorreto e senha correta"""
        self.iniciar_teste("Rejeitar usuario incorreto com senha correta")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            digitar_texto("usuario_errado")
            pressionar_tecla("tab")
            digitar_texto("123456")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve continuar na tela de login
            sucesso = verificar_imagem_visivel("login_screen.png")
            registrar_teste(
                "Rejeitar usuario incorreto com senha correta",
                sucesso,
                "Deveria rejeitar usuario incorreto" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_multiplas_tentativas_login(self):
        """Deve permitir múltiplas tentativas de login"""
        self.iniciar_teste("Multiplas tentativas de login")
        
        app = iniciar_aplicacao()
        
        try:
            aguardar_imagem("login_screen.png")
            
            # Primeira tentativa - falha
            digitar_texto("usuario_errado")
            pressionar_tecla("tab")
            digitar_texto("senha_errada")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Limpa campos se houver mensagem de erro
            if verificar_imagem_visivel("error_message.png", confianca=0.7):
                pressionar_tecla("enter")  # Fecha mensagem de erro
                time.sleep(0.5)
            
            # Limpa campos
            pyautogui.hotkey('ctrl', 'a')
            pressionar_tecla('delete')
            
            # Segunda tentativa - sucesso
            digitar_texto("admin")
            pressionar_tecla("tab")
            digitar_texto("123456")
            pressionar_tecla("enter")
            
            time.sleep(2)
            
            # Deve conseguir logar
            sucesso = aguardar_imagem("main_interface.png", timeout=5)
            registrar_teste(
                "Multiplas tentativas de login",
                sucesso,
                "Deveria permitir login apos tentativa falha" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)

# Função para executar os testes deste módulo isoladamente
if __name__ == "__main__":
    # Verifica imagens necessárias
    imagens_faltando = verificar_imagens_necessarias()
    
    if imagens_faltando:
        print("ATENCAO: Imagens necessarias nao encontradas:")
        for img in imagens_faltando:
            print(f"   - {DIRETORIO_SCREENSHOTS / img}")
        print("\nExecute a aplicacao manualmente e capture estas telas.")
        print("Use: pyautogui.screenshot('caminho/para/imagem.png')")
        sys.exit(1)
    
    # Inicia relatório
    nome_arquivo = iniciar_relatorio("Teste_Login")
    
    # Executa testes
    testes = TestesLogin()
    testes.executar_todos_testes()
    
    # Fecha relatório
    fechar_relatorio()
    
    # Exibe estatísticas
    stats = obter_estatisticas()
    print(f"\nRelatorio salvo em: {nome_arquivo}")
    print(f"Taxa de sucesso: {stats['taxa_sucesso']:.1f}%")