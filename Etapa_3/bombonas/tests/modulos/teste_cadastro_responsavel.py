"""
Módulo de testes de cadastro de responsável
Testa todas as funcionalidades relacionadas ao cadastro de responsáveis
"""

import time
from base_teste import *

class TestesCadastroResponsavel(TesteBase):
    """Testes de cadastro de responsáveis"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de cadastro"""
        self.testar_criar_responsavel_valido()
        self.testar_rejeitar_cpf_invalido()
        self.testar_rejeitar_cpf_tamanho_incorreto()
        self.testar_rejeitar_cpf_com_mais_digitos()
        self.testar_rejeitar_campos_vazios_responsavel()
        self.testar_rejeitar_nome_vazio()
        self.testar_rejeitar_telefone_vazio()
        self.testar_rejeitar_setor_vazio()
        self.testar_rejeitar_nome_apenas_numeros()
        self.testar_rejeitar_telefone_com_letras()
    
    def testar_criar_responsavel_valido(self):
        """Deve criar um novo responsável com dados válidos"""
        self.iniciar_teste("Criar responsavel valido")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
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
                "Criar responsavel com dados validos",
                sucesso,
                "Mensagem de sucesso nao apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_cpf_invalido(self):
        """Deve rejeitar CPF inválido"""
        self.iniciar_teste("Rejeitar CPF invalido")
        
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
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar CPF invalido (digitos iguais)",
                sucesso,
                "Deveria rejeitar CPF com todos digitos iguais" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_cpf_tamanho_incorreto(self):
        """Deve rejeitar CPF com tamanho incorreto"""
        self.iniciar_teste("Rejeitar CPF com tamanho incorreto")
        
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
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar CPF com menos de 11 digitos",
                sucesso,
                "Deveria rejeitar CPF com tamanho incorreto" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_cpf_com_mais_digitos(self):
        """Deve rejeitar CPF com mais de 11 dígitos"""
        self.iniciar_teste("Rejeitar CPF com mais de 11 digitos")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            # CPF com mais de 11 dígitos
            digitar_texto("123456789012345")
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
                "Rejeitar CPF com mais de 11 digitos",
                sucesso,
                "Deveria rejeitar CPF com mais de 11 digitos" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_campos_vazios_responsavel(self):
        """Deve rejeitar cadastro com campos vazios"""
        self.iniciar_teste("Rejeitar campos vazios no cadastro de responsavel")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            # Tenta cadastrar sem preencher nada
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
    
    def testar_rejeitar_nome_vazio(self):
        """Deve rejeitar cadastro com nome vazio"""
        self.iniciar_teste("Rejeitar nome vazio")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            # Não digita nome
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro com nome vazio",
                sucesso,
                "Deveria rejeitar cadastro sem nome" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_telefone_vazio(self):
        """Deve rejeitar cadastro com telefone vazio"""
        self.iniciar_teste("Rejeitar telefone vazio")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            # Não digita telefone
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro com telefone vazio",
                sucesso,
                "Deveria rejeitar cadastro sem telefone" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_setor_vazio(self):
        """Deve rejeitar cadastro com setor vazio"""
        self.iniciar_teste("Rejeitar setor vazio")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            # Não digita setor
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar cadastro com setor vazio",
                sucesso,
                "Deveria rejeitar cadastro sem setor" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_nome_apenas_numeros(self):
        """Deve rejeitar nome contendo apenas números"""
        self.iniciar_teste("Rejeitar nome apenas com numeros")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            digitar_texto("123456")  # Nome apenas números
            pressionar_tecla("tab")
            digitar_texto("11999887766")
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar nome apenas com numeros",
                sucesso,
                "Deveria rejeitar nome contendo apenas numeros" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_rejeitar_telefone_com_letras(self):
        """Deve rejeitar telefone contendo letras"""
        self.iniciar_teste("Rejeitar telefone com letras")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_cadastrar_responsavel.png")
            time.sleep(1)
            
            digitar_texto("12345678909")  # CPF válido
            pressionar_tecla("tab")
            digitar_texto("Nome Teste")
            pressionar_tecla("tab")
            digitar_texto("119ABC87766")  # Telefone com letras
            pressionar_tecla("tab")
            digitar_texto("SETOR")
            
            pressionar_tecla("enter")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
            registrar_teste(
                "Rejeitar telefone com letras",
                sucesso,
                "Deveria rejeitar telefone contendo letras" if not sucesso else ""
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
    nome_arquivo = iniciar_relatorio("Teste_Cadastro_Responsavel")
    
    # Executa testes
    testes = TestesCadastroResponsavel()
    testes.executar_todos_testes()
    
    # Fecha relatório
    fechar_relatorio()
    
    # Exibe estatísticas
    stats = obter_estatisticas()
    print(f"\nRelatorio salvo em: {nome_arquivo}")
    print(f"Taxa de sucesso: {stats['taxa_sucesso']:.1f}%")