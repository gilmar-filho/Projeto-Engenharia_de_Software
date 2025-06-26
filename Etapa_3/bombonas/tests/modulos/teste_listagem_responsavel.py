"""
Módulo de testes de listagem de responsável
Testa funcionalidades de listagem, edição e exclusão de responsáveis
"""

import time
import pyautogui
from base_teste import *

class TestesListagemResponsavel(TesteBase):
    """Testes de listagem, edição e exclusão de responsáveis"""
    
    def executar_todos_testes(self):
        """Executa todos os testes de listagem"""
        self.testar_listar_responsaveis()
        self.testar_editar_responsavel()
        self.testar_editar_responsavel_nome_vazio()
        self.testar_editar_responsavel_telefone_vazio()
        self.testar_editar_responsavel_setor_vazio()
        self.testar_editar_responsavel_telefone_invalido()
        self.testar_remover_responsavel_sem_bombonas()
        self.testar_cancelar_remocao_responsavel()
        self.testar_duplo_clique_editar()
        self.testar_tecla_delete_remover()
    
    def testar_listar_responsaveis(self):
        """Deve listar responsáveis cadastrados"""
        self.iniciar_teste("Listar responsaveis")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            sucesso = verificar_imagem_visivel("lista_responsaveis.png") or verificar_imagem_visivel("table_header.png")
            registrar_teste(
                "Listar responsaveis",
                sucesso,
                "Lista de responsaveis nao apareceu" if not sucesso else ""
            )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel(self):
        """Deve editar um responsável existente"""
        self.iniciar_teste("Editar responsavel")
        
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
                    "Editar responsavel",
                    sucesso,
                    "Nao conseguiu editar responsavel" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Editar responsavel",
                    False,
                    "Botao editar nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel_nome_vazio(self):
        """Deve rejeitar edição com nome vazio"""
        self.iniciar_teste("Rejeitar edicao com nome vazio")
        
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
                    "Rejeitar edicao com nome vazio",
                    sucesso,
                    "Deveria rejeitar nome vazio na edicao" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Rejeitar edicao com nome vazio",
                    False,
                    "Botao editar nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel_telefone_vazio(self):
        """Deve rejeitar edição com telefone vazio"""
        self.iniciar_teste("Rejeitar edicao com telefone vazio")
        
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
                
                # Vai até o campo telefone
                pressionar_tecla("tab")  # Pula CPF
                pressionar_tecla("tab")  # Pula nome
                pyautogui.hotkey('ctrl', 'a')
                pressionar_tecla('delete')
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Rejeitar edicao com telefone vazio",
                    sucesso,
                    "Deveria rejeitar telefone vazio na edicao" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Rejeitar edicao com telefone vazio",
                    False,
                    "Botao editar nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel_setor_vazio(self):
        """Deve rejeitar edição com setor vazio"""
        self.iniciar_teste("Rejeitar edicao com setor vazio")
        
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
                
                # Vai até o campo setor
                pressionar_tecla("tab")  # Pula CPF
                pressionar_tecla("tab")  # Pula nome
                pressionar_tecla("tab")  # Pula telefone
                pyautogui.hotkey('ctrl', 'a')
                pressionar_tecla('delete')
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Rejeitar edicao com setor vazio",
                    sucesso,
                    "Deveria rejeitar setor vazio na edicao" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Rejeitar edicao com setor vazio",
                    False,
                    "Botao editar nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_editar_responsavel_telefone_invalido(self):
        """Deve rejeitar edição com telefone inválido"""
        self.iniciar_teste("Rejeitar edicao com telefone invalido")
        
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
                
                # Vai até o campo telefone
                pressionar_tecla("tab")  # Pula CPF
                pressionar_tecla("tab")  # Pula nome
                pyautogui.hotkey('ctrl', 'a')
                digitar_texto("ABC123")  # Telefone com letras
                
                pressionar_tecla("enter")
                time.sleep(2)
                
                sucesso = verificar_imagem_visivel("error_message.png") or not verificar_imagem_visivel("success_message.png")
                registrar_teste(
                    "Rejeitar edicao com telefone invalido",
                    sucesso,
                    "Deveria rejeitar telefone com letras na edicao" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Rejeitar edicao com telefone invalido",
                    False,
                    "Botao editar nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_remover_responsavel_sem_bombonas(self):
        """Deve remover responsável que não possui bombonas"""
        self.iniciar_teste("Remover responsavel sem bombonas")
        
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
                    "Remover responsavel sem bombonas",
                    sucesso,
                    "Nao conseguiu remover responsavel" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Remover responsavel sem bombonas",
                    False,
                    "Botao excluir nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_cancelar_remocao_responsavel(self):
        """Deve cancelar remoção quando solicitado"""
        self.iniciar_teste("Cancelar remocao de responsavel")
        
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
            
            # Clica em excluir
            if clicar_imagem("btn_excluir.png"):
                time.sleep(1)
                
                # Cancela exclusão (Tab para ir ao botão Não/Cancelar)
                pressionar_tecla("tab")
                time.sleep(0.2)
                pressionar_tecla("enter")
                time.sleep(1)
                
                # Verifica se ainda está na lista
                sucesso = verificar_imagem_visivel("lista_responsaveis.png") or verificar_imagem_visivel("table_header.png")
                registrar_teste(
                    "Cancelar remocao de responsavel",
                    sucesso,
                    "Deveria continuar na lista apos cancelar" if not sucesso else ""
                )
            else:
                registrar_teste(
                    "Cancelar remocao de responsavel",
                    False,
                    "Botao excluir nao encontrado"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_duplo_clique_editar(self):
        """Deve abrir edição com duplo clique no item"""
        self.iniciar_teste("Editar com duplo clique")
        
        app = iniciar_aplicacao()
        
        try:
            fazer_login()
            
            # Lista responsáveis
            clicar_imagem("btn_listar_responsaveis.png")
            time.sleep(2)
            
            # Tenta duplo clique no primeiro item
            if verificar_imagem_visivel("first_list_item.png", confianca=0.7):
                clicar_imagem("first_list_item.png", confianca=0.7)
                time.sleep(0.3)
                clicar_imagem("first_list_item.png", confianca=0.7)
                time.sleep(1)
                
                # Verifica se abriu tela de edição
                sucesso = verificar_imagem_visivel("edit_form.png", confianca=0.7) or aguardar_imagem("btn_salvar.png", timeout=3)
                registrar_teste(
                    "Editar com duplo clique",
                    sucesso,
                    "Duplo clique nao abriu edicao" if not sucesso else ""
                )
                
                # Fecha se abriu
                if sucesso:
                    pressionar_tecla("escape")
            else:
                registrar_teste(
                    "Editar com duplo clique",
                    False,
                    "Nao encontrou item na lista"
                )
            
        finally:
            parar_aplicacao(app)
    
    def testar_tecla_delete_remover(self):
        """Deve abrir confirmação de exclusão com tecla Delete"""
        self.iniciar_teste("Remover com tecla Delete")
        
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
            
            # Pressiona Delete
            pressionar_tecla("delete")
            time.sleep(1)
            
            # Verifica se abriu confirmação
            sucesso = verificar_imagem_visivel("confirm_dialog.png", confianca=0.7) or verificar_imagem_visivel("dialog_box.png", confianca=0.7)
            registrar_teste(
                "Remover com tecla Delete",
                sucesso,
                "Tecla Delete nao abriu confirmacao" if not sucesso else ""
            )
            
            # Cancela se abriu
            if sucesso:
                pressionar_tecla("escape")
            
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
    nome_arquivo = iniciar_relatorio("Teste_Listagem_Responsavel")
    
    # Executa testes
    testes = TestesListagemResponsavel()
    testes.executar_todos_testes()
    
    # Fecha relatório
    fechar_relatorio()
    
    # Exibe estatísticas
    stats = obter_estatisticas()
    print(f"\nRelatorio salvo em: {nome_arquivo}")
    print(f"Taxa de sucesso: {stats['taxa_sucesso']:.1f}%")