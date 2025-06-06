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
        self.root.geometry("800x600")
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
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
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
        """Cria o menu principal."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Responsáveis
        menu_responsaveis = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Responsáveis", menu=menu_responsaveis)
        menu_responsaveis.add_command(
            label="Cadastrar Responsável", 
            command=self._abrir_cadastro_responsavel
        )
        menu_responsaveis.add_command(
            label="Listar Responsáveis", 
            command=self._abrir_listagem_responsaveis
        )
        
        # Menu Bombonas
        menu_bombonas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bombonas", menu=menu_bombonas)
        menu_bombonas.add_command(
            label="Cadastrar Bombona", 
            command=self._abrir_cadastro_bombona
        )
        menu_bombonas.add_command(
            label="Listar Bombonas", 
            command=self._abrir_listagem_bombonas
        )
        
        # Menu Relatórios
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_relatorios.add_command(
            label="Gerar Relatório", 
            command=self._abrir_relatorios
        )
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)
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
        botoes_frame.pack(pady=20)
        
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
        
        # Área de estatísticas
        self._criar_area_estatisticas(main_frame)
        
        # Botão sair
        ttk.Button(
            main_frame,
            text="Sair do Sistema",
            command=self._sair_aplicacao,
            width=20
        ).pack(pady=(20, 0))
    
    def _criar_area_estatisticas(self, parent):
        """Cria a área de estatísticas."""
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas do Sistema", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Text widget para estatísticas
        text_frame = ttk.Frame(stats_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_text = tk.Text(text_frame, height=10, width=70, state='disabled', wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar.set)
        
        self.stats_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para atualizar estatísticas
        ttk.Button(
            stats_frame, 
            text="Atualizar Estatísticas", 
            command=self._atualizar_estatisticas
        ).pack(pady=(10, 0))
        
        # Carrega estatísticas iniciais
        self._atualizar_estatisticas()
    
    def _atualizar_estatisticas(self):
        """Atualiza as estatísticas exibidas."""
        try:
            # Limpar texto
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            
            # Verificar se os métodos existem antes de chamar
            try:
                # Tentar obter estatísticas dos controllers
                if hasattr(self.bombona_controller, 'get_estatisticas'):
                    stats_bombonas = self.bombona_controller.get_estatisticas()
                else:
                    # Fallback: obter dados básicos
                    bombonas = self.bombona_controller.listarBombonas()
                    stats_bombonas = {
                        'total_bombonas': len(bombonas),
                        'volume_total': sum(b.getVolume() for b in bombonas),
                        'volume_medio': sum(b.getVolume() for b in bombonas) / len(bombonas) if bombonas else 0,
                        'tipos_residuo': {}
                    }
                    # Contar tipos
                    for b in bombonas:
                        tipo = b.getTipoResiduo()
                        stats_bombonas['tipos_residuo'][tipo] = stats_bombonas['tipos_residuo'].get(tipo, 0) + 1
                
                if hasattr(self.responsavel_controller, 'get_estatisticas'):
                    stats_responsaveis = self.responsavel_controller.get_estatisticas()
                else:
                    # Fallback: obter dados básicos
                    responsaveis = self.responsavel_controller.listarResponsaveis()
                    stats_responsaveis = {
                        'total_responsaveis': len(responsaveis),
                        'responsaveis_por_setor': {}
                    }
                    # Contar por setor
                    for r in responsaveis:
                        setor = r.getSetor()
                        stats_responsaveis['responsaveis_por_setor'][setor] = stats_responsaveis['responsaveis_por_setor'].get(setor, 0) + 1
                
                # Construir texto das estatísticas
                texto = f"""ESTATÍSTICAS DO SISTEMA
{'='*50}

BOMBONAS:
• Total de bombonas: {stats_bombonas['total_bombonas']}
• Volume total: {stats_bombonas['volume_total']:.1f} L
• Volume médio: {stats_bombonas['volume_medio']:.1f} L

RESPONSÁVEIS:
• Total de responsáveis: {stats_responsaveis['total_responsaveis']}

BOMBONAS POR TIPO DE RESÍDUO:
"""
                
                for tipo, qtd in stats_bombonas['tipos_residuo'].items():
                    texto += f"• {tipo}: {qtd} bombona(s)\n"
                
                texto += "\nRESPONSÁVEIS POR SETOR:\n"
                for setor, qtd in stats_responsaveis['responsaveis_por_setor'].items():
                    texto += f"• {setor}: {qtd} responsável(is)\n"
                
                self.stats_text.insert(1.0, texto)
                
            except Exception as e:
                self.stats_text.insert(1.0, f"Erro ao carregar estatísticas: {e}\n\nVerifique se os controllers estão implementados corretamente.")
            
            self.stats_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {e}")
    
    # Métodos para abrir as diferentes telas
    def _abrir_cadastro_responsavel(self):
        """Abre a tela de cadastro de responsável."""
        try:
            from views.tela_cadastro_responsavel import TelaCadastroResponsavel
            tela = TelaCadastroResponsavel(self.root, self.responsavel_controller)
            tela.exibir_formulario()
            # Atualiza estatísticas após fechar a tela
            self.root.after(1000, self._atualizar_estatisticas)
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
            self.root.after(1000, self._atualizar_estatisticas)
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
    
    def _abrir_relatorios(self):
        """Abre a tela de relatórios."""
        try:
            from views.tela_relatorio import TelaRelatorio
            tela = TelaRelatorio(
                self.root, 
                self.bombona_controller, 
                self.responsavel_controller
            )
            tela.exibir_tela()
        except ImportError:
            messagebox.showerror("Erro", "Módulo tela_relatorio não encontrado.\nVerifique se o arquivo está no diretório views/")
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