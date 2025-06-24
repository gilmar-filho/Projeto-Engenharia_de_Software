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

class SistemaBombonas:
    """
    Classe principal que inicializa e coordena o sistema.
    """

    def __init__(self):
        """Inicializa o sistema."""
        self.root = None
        self.janela_login = None

    def _iniciar_sistema_principal(self):
        """Inicia o sistema principal após login bem-sucedido."""
        try:
            self.criar_interface()
            self.root.protocol("WM_DELETE_WINDOW", self._sair_aplicacao)
            self.root.mainloop()

        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Erro ao iniciar sistema principal:\n{e}")

    def criar_interface(self):
        """Cria a interface gráfica principal."""
        self.root = tk.Tk()
        self.root.title("Sistema de Gerenciamento de Bombonas")
        self.root.geometry("600x700")
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

        # Menu Ajuda
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

    def _abrir_cadastro_responsavel(self):
        """Abre a tela de cadastro de responsável."""
        try:
            from views.tela_cadastro_responsavel import TelaCadastroResponsavel
            tela = TelaCadastroResponsavel(self.root)
            tela.exibir_formulario()
        except ImportError as e:
            messagebox.showerror(f"Erro: {e}\nMódulo tela_cadastro_responsavel com problemas de importação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de cadastro de responsável:\n{e}")

    def _abrir_listagem_responsaveis(self):
        """Abre a tela de listagem de responsáveis."""
        try:
            from views.tela_listagem_responsaveis import TelaListagemResponsaveis
            tela = TelaListagemResponsaveis(self.root)
            tela.exibir_lista()
        except ImportError:
            messagebox.showerror(f"Erro: {e}\nMódulo tela_listagem_responsaveis com problemas de importação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de listagem de responsáveis:\n{e}")

    def _abrir_cadastro_bombona(self):
        """Abre a tela de cadastro de bombona."""
        try:
            from views.tela_cadastro_bombona import TelaCadastroBombona
            tela = TelaCadastroBombona(self.root)
            tela.exibir_formulario()
        except ImportError as e:
            messagebox.showerror(f"Erro: {e}\nMódulo tela_cadastro_bombona com problemas de importação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de cadastro de bombona:\n{e}")

    def _abrir_listagem_bombonas(self):
        """Abre a tela de listagem de bombonas."""
        try:
            from views.tela_listagem_bombonas import TelaListagemBombonas
            tela = TelaListagemBombonas(self.root)
            tela.exibir_lista()
        except ImportError as e:
            messagebox.showerror(f"Erro: {e}\nMódulo tela_listagem_bombonas com problemas de importação.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de listagem de bombonas:\n{e}")

    def _abrir_relatorios(self):
        """Abre a tela de relatórios."""
        try:
            from views.tela_relatorio import TelaRelatorio
            tela = TelaRelatorio(self.root)
            tela.exibir_tela()
        except ImportError as e:
            messagebox.showerror(f"Erro: {e}\nMódulo tela_relatorio com problemas de importação.")
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
        """Executa o sistema iniciando pela tela de login."""
        try:
            print("Iniciando sistema com tela de login...")

            # Importa a Tela de Login das views
            from views.tela_login import TelaLogin
        
            # Cria e exibe a tela de login
            tela_login = TelaLogin(
                callback_sucesso=self._iniciar_sistema_principal
            )
            tela_login.exibir_login()

        except ImportError as e:
            print(f"Erro ao importar módulos: {e}")
            print("Certifique-se de que todos os módulos estão implementados conforme o diagrama UML")
            sys.exit(1)

        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Erro ao executar sistema: {e}")

def main():
    """Função principal."""
    try:
        print("Iniciando Sistema de Gerenciamento de Bombonas...")
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
