"""
Arquivo principal do Sistema de Gerenciamento de Bombonas de Resíduos Químicos
Versão corrigida para compatibilidade com interfaces simplificadas
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Adiciona o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações das camadas do sistema
try:
    from dao.responsavel_dao import ResponsavelDAO
    from dao.bombona_dao import BombonaDAO
    from controllers.responsavel_controller import ResponsavelController
    from controllers.bombona_controller import BombonaController
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todos os módulos estão implementados conforme o diagrama UML")
    sys.exit(1)


class SistemaBombonas:
    """
    Classe principal que inicializa e coordena o sistema.
    """
    
    def __init__(self):
        """Inicializa o sistema."""
        self.root = None
        self.responsavel_dao = None
        self.bombona_dao = None
        self.responsavel_controller = None
        self.bombona_controller = None
        
        self._inicializar_sistema()
    
    def _inicializar_sistema(self):
        """Inicializa os componentes do sistema."""
        try:
            # Inicializa os DAOs
            self.responsavel_dao = ResponsavelDAO()
            self.bombona_dao = BombonaDAO()
            
            # Inicializa os Controllers
            self.responsavel_controller = ResponsavelController(
                self.responsavel_dao, 
                self.bombona_dao
            )
            self.bombona_controller = BombonaController(
                self.bombona_dao, 
                self.responsavel_dao
            )
            
            print("Sistema inicializado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao inicializar sistema: {e}")
            messagebox.showerror("Erro de Inicialização", 
                f"Não foi possível inicializar o sistema:\n{e}\n\n"
                "Verifique se todos os componentes estão implementados corretamente.")
            sys.exit(1)
    
    def criar_interface(self):
        """Cria a interface gráfica principal."""
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento de Bombonas")
        self.root.geometry("600x700")  # Aumentado de 800x600 para 900x700
        self.root.resizable(True, True)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Configura o estilo
        self._configurar_estilo()
        
        # Cria o menu principal
        self._criar_menu()
        
        # Cria a tela principal
        self._criar_tela_principal()
        
        return self.root
    
    def _centralizar_janela(self):
        """Posiciona a janela no centro-superior da tela."""
        self.root.update_idletasks()
        
        # Obtém dimensões da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        
        # Dimensões da janela
        largura_janela = 600
        altura_janela = 700
        
        # Calcula posição X (centro horizontal)
        x = (largura_tela - largura_janela) // 2
        
        # Calcula posição Y (parte superior - aproximadamente 15% da altura da tela)
        y = int(altura_tela * 0.15)  # 15% do topo da tela
        
        # Define a posição da janela
        self.root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    
    def _configurar_estilo(self):
        """Configura o estilo da interface."""
        try:
            style = ttk.Style()
            style.theme_use('clam')  # Tema moderno
            
            # Configura cores personalizadas
            style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
            style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
            style.configure('Info.TLabel', font=('Arial', 10))
        except tk.TclError:
            # Se o tema não estiver disponível, usa o padrão
            style = ttk.Style()
            style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
            style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
            style.configure('Info.TLabel', font=('Arial', 10))
    
    def _criar_menu(self):
        """Cria o menu principal simplificado."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Adiciona espaços vazios para empurrar o menu Ajuda para a direita
        # Isso é uma técnica simples para alinhar à direita
        menubar.add_command(label="", state="disabled")  # Espaço invisível
        
        # Menu Ajuda (alinhado à direita)
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="Sair", command=self._sair_aplicacao)
    
    def _criar_tela_principal(self):
        """Cria a tela principal do sistema."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Sistema de Gerenciamento de Bombonas", 
            style='Title.TLabel'
        )
        titulo.pack(pady=(0, 30))
        
        # Subtítulo
        subtitulo = ttk.Label(
            main_frame,
            text="Selecione uma opção:",
            style='Subtitle.TLabel'
        )
        subtitulo.pack(pady=(0, 20))
        
        # Frame para botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(expand=True)  # Centraliza verticalmente
        
        # Seção Responsáveis
        resp_frame = ttk.LabelFrame(botoes_frame, text="Responsáveis", padding="15")
        resp_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            resp_frame, 
            text="Cadastrar Responsável", 
            command=self._abrir_cadastro_responsavel,
            width=25
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            resp_frame, 
            text="Listar Responsáveis", 
            command=self._abrir_listagem_responsaveis,
            width=25
        ).pack(side=tk.LEFT)
        
        # Seção Bombonas
        bomb_frame = ttk.LabelFrame(botoes_frame, text="Bombonas", padding="15")
        bomb_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            bomb_frame, 
            text="Cadastrar Bombona", 
            command=self._abrir_cadastro_bombona,
            width=25
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            bomb_frame, 
            text="Listar Bombonas", 
            command=self._abrir_listagem_bombonas,
            width=25
        ).pack(side=tk.LEFT)
        
        # Seção Relatórios
        rel_frame = ttk.LabelFrame(botoes_frame, text="Relatórios", padding="15")
        rel_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(
            rel_frame, 
            text="Gerar Relatórios", 
            command=self._abrir_relatorios,
            width=25
        ).pack()
        
        # Botão sair
        ttk.Button(
            main_frame,
            text="Sair do Sistema",
            command=self._sair_aplicacao,
            width=20
        ).pack(pady=(30, 0))
    
#     def _criar_area_estatisticas(self, parent):
#         """Cria a área de estatísticas."""
#         stats_frame = ttk.LabelFrame(parent, text="Estatísticas do Sistema", padding="15")
#         stats_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))  # Reduzido de 20 para 15
        
#         # Text widget para estatísticas - altura aumentada
#         text_frame = ttk.Frame(stats_frame)
#         text_frame.pack(fill=tk.BOTH, expand=True)
        
#         self.stats_text = tk.Text(text_frame, height=15, width=80, state='disabled', wrap=tk.WORD, font=('Arial', 10))  # Aumentado height de 10 para 15, width de 70 para 80
#         scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.stats_text.yview)
#         self.stats_text.configure(yscrollcommand=scrollbar.set)
        
#         self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         # Botão para atualizar estatísticas
#         ttk.Button(
#             stats_frame, 
#             text="Atualizar Estatísticas", 
#             command=self._atualizar_estatisticas
#         ).pack(pady=(15, 0))  # Aumentado de 10 para 15
        
#         # Carrega estatísticas iniciais
#         self._atualizar_estatisticas()
    
#     def _atualizar_estatisticas(self):
#         """Atualiza as estatísticas exibidas."""
#         try:
#             # Limpar texto
#             self.stats_text.config(state='normal')
#             self.stats_text.delete(1.0, tk.END)
            
#             try:
#                 # Obter estatísticas básicas
#                 responsaveis = self.responsavel_controller.listar_responsaveis()
#                 bombonas = self.bombona_controller.listar_bombonas()
                
#                 total_responsaveis = len(responsaveis)
#                 total_bombonas = len(bombonas)
                
#                 # Construir texto das estatísticas sem volumes
#                 texto = f"""ESTATÍSTICAS DO SISTEMA
# {'='*50}

# BOMBONAS:
# • Total de bombonas: {total_bombonas}

# RESPONSÁVEIS:
# • Total de responsáveis: {total_responsaveis}

# BOMBONAS POR TIPO DE RESÍDUO:
# """
                
#                 # Contar tipos de resíduo
#                 tipos_residuo = {}
#                 for b in bombonas:
#                     tipo = b.get_tipo_residuo()
#                     tipos_residuo[tipo] = tipos_residuo.get(tipo, 0) + 1
                
#                 for tipo, qtd in tipos_residuo.items():
#                     texto += f"• {tipo}: {qtd} bombona(s)\n"
                
#                 texto += "\nRESPONSÁVEIS POR SETOR:\n"
                
#                 # Contar responsáveis por setor
#                 setores = {}
#                 for r in responsaveis:
#                     setor = r.get_setor()
#                     setores[setor] = setores.get(setor, 0) + 1
                
#                 for setor, qtd in setores.items():
#                     texto += f"• {setor}: {qtd} responsável(is)\n"
                
#                 # Bombonas por setor
#                 texto += "\nBOMBONAS POR SETOR:\n"
#                 bombonas_por_setor = {}
#                 for b in bombonas:
#                     if b.get_responsavel():
#                         setor = b.get_responsavel().get_setor()
#                         bombonas_por_setor[setor] = bombonas_por_setor.get(setor, 0) + 1
                
#                 for setor, qtd in bombonas_por_setor.items():
#                     texto += f"• {setor}: {qtd} bombona(s)\n"
                
#                 self.stats_text.insert(1.0, texto)
                
#             except Exception as e:
#                 self.stats_text.insert(1.0, f"Erro ao carregar estatísticas: {e}\n\nVerifique se os controllers estão implementados corretamente.")
            
#             self.stats_text.config(state='disabled')
            
#         except Exception as e:
#             messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {e}")
    
    # Métodos para abrir as diferentes telas
    def _abrir_cadastro_responsavel(self):
        """Abre a tela de cadastro de responsável."""
        try:
            from views.tela_cadastro_responsavel import TelaCadastroResponsavel
            tela = TelaCadastroResponsavel(self.root, self.responsavel_controller)
            tela.exibir_formulario()
            # Atualiza estatísticas após fechar a tela
            # self.root.after(1000, self._atualizar_estatisticas)
        except ImportError:
            messagebox.showerror("Erro", "Módulo tela_cadastro_responsavel não encontrado.\nVerifique se o arquivo está no diretório views/")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de cadastro de responsável:\n{e}")
    
    def _abrir_listagem_responsaveis(self):
        """Abre a tela de listagem de responsáveis."""
        try:
            from views.tela_listagem_responsaveis import TelaListagemResponsaveis
            tela = TelaListagemResponsaveis(self.root, self.responsavel_controller)
            tela.exibir_lista()
        except ImportError:
            messagebox.showerror("Erro", "Módulo tela_listagem_responsaveis não encontrado.\nVerifique se o arquivo está no diretório views/")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de listagem de responsáveis:\n{e}")
    
    def _abrir_cadastro_bombona(self):
        """Abre a tela de cadastro de bombona."""
        try:
            from views.tela_cadastro_bombona import TelaCadastroBombona
            tela = TelaCadastroBombona(
                self.root, 
                self.bombona_controller, 
                self.responsavel_controller
            )
            tela.exibir_formulario()
            # Atualiza estatísticas após fechar a tela
            # self.root.after(1000, self._atualizar_estatisticas)
        except ImportError:
            messagebox.showerror("Erro", "Módulo tela_cadastro_bombona não encontrado.\nVerifique se o arquivo está no diretório views/")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de cadastro de bombona:\n{e}")
    
    def _abrir_listagem_bombonas(self):
        """Abre a tela de listagem de bombonas."""
        try:
            from views.tela_listagem_bombonas import TelaListagemBombonas
            tela = TelaListagemBombonas(
                self.root, 
                self.bombona_controller,
                self.responsavel_controller  # Passa o ResponsavelController
            )
            tela.exibir_lista()
        except ImportError:
            messagebox.showerror("Erro", "Módulo tela_listagem_bombonas não encontrado.\nVerifique se o arquivo está no diretório views/")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de listagem de bombonas:\n{e}")
    
    """
    Alterações simples no main.py para integrar a nova tela de relatórios
    Substituir apenas o método _abrir_relatorios() no arquivo main.py existente
    """

    # Substituir este método na classe SistemaBombonas:

    def _abrir_relatorios(self):
        """Abre a tela de relatórios."""
        try:
            # Verifica se há dados mínimos
            responsaveis = self.responsavel_controller.listar_responsaveis()
            bombonas = self.bombona_controller.listar_bombonas()
            
            if not responsaveis and not bombonas:
                messagebox.showwarning(
                    "Aviso", 
                    "Não há dados para gerar relatórios.\n"
                    "Cadastre pelo menos alguns responsáveis e bombonas primeiro."
                )
                return
            
            # Importa e abre a tela de relatórios
            from views.tela_relatorio import TelaRelatorio
            tela = TelaRelatorio(
                self.root, 
                self.bombona_controller, 
                self.responsavel_controller
            )
            tela.exibir_tela()
            
        except ImportError:
            messagebox.showerror(
                "Erro", 
                "Módulo tela_relatorio não encontrado.\n"
                "Verifique se o arquivo está no diretório views/"
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de relatórios:\n{e}")
    
    def _mostrar_sobre(self):
        """Mostra informações sobre o sistema."""
        sobre_texto = """Sistema de Gerenciamento de Bombonas de Resíduos Químicos
        
                        Versão: 1.0
                        Desenvolvido para a disciplina de Engenharia de Software

                        Funcionalidades:
                        • Cadastro e gerenciamento de responsáveis
                        • Cadastro e gerenciamento de bombonas
                        • Geração de relatórios
                        • Controle de acesso aos dados

                        Arquitetura:
                        • Padrão MVC (Model-View-Controller)
                        • Padrão DAO (Data Access Object)
                        • Padrão Factory Method
                        • Interface gráfica com Tkinter
                        • Persistência em arquivos

                        Requisitos:
                        • Python 3.6+
                        • Tkinter (incluído no Python)
                        • Estrutura de pastas: dao/, controllers/, views/, models/"""
        
        messagebox.showinfo("Sobre o Sistema", sobre_texto)
    
    def _sair_aplicacao(self):
        """Sai da aplicação com confirmação."""
        resposta = messagebox.askyesno(
            "Confirmar Saída",
            "Tem certeza que deseja sair do sistema?"
        )
        
        if resposta:
            self.root.destroy()
    
    def executar(self):
        """Executa o sistema."""
        try:
            self.criar_interface()
            
            # Bind para capturar fechamento da janela
            self.root.protocol("WM_DELETE_WINDOW", self._sair_aplicacao)
            
            # Inicia o loop principal
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Erro ao executar sistema: {e}")


def verificar_estrutura_projeto():
    """Verifica se a estrutura básica do projeto existe."""
    diretorios_necessarios = ['dao', 'controllers', 'views', 'models']
    
    for diretorio in diretorios_necessarios:
        if not os.path.exists(diretorio):
            print(f"Aviso: Diretório '{diretorio}' não encontrado.")
            print(f"Crie o diretório ou verifique a estrutura do projeto.")


def main():
    """Função principal."""
    try:
        print("Iniciando Sistema de Gerenciamento de Bombonas...")
        print("Verificando estrutura do projeto...")
        
        # Verifica estrutura básica
        verificar_estrutura_projeto()
        
        print("Criando instância do sistema...")
        
        # Cria e executa o sistema
        sistema = SistemaBombonas()
        
        print("Executando interface gráfica...")
        sistema.executar()
        
        print("Sistema encerrado.")
        
    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {e}")
        messagebox.showerror("Erro Fatal", 
            f"Erro fatal ao inicializar o sistema:\n{e}\n\n"
            "Verifique se todos os módulos estão implementados corretamente.")
        sys.exit(1)


if __name__ == "__main__":
    main()