"""
Tela de cadastro de bombona - Versão Simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox

class TelaCadastroBombona:
    """
    Tela simplificada para cadastrar novas bombonas.
    """

    def __init__(self, parent):
        """ Inicializa a tela de cadastro. """
        self.parent = parent
        self.janela = None
        
        # View cria seus próprios controllers (autonomia)
        from controllers.bombona_controller import BombonaController
        from controllers.responsavel_controller import ResponsavelController
        
        self.bombona_controller = BombonaController()
        self.responsavel_controller = ResponsavelController()
        
        # Variáveis dos campos
        self.var_codigo = tk.StringVar()
        self.var_volume = tk.StringVar()
        self.var_tipo_residuo = tk.StringVar()
        self.var_responsavel = tk.StringVar()
        
        # Lista de responsáveis
        self.responsaveis_dict = {}
    
    def exibir_formulario(self):
        """ Exibe a tela de cadastro. """
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Cadastro de Bombona")
        self.janela.geometry("450x400")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Carrega responsáveis
        if not self._carregar_responsaveis():
            return
        
        # Cria o formulário
        self._criar_formulario()
        
        # Foca no primeiro campo
        self.entry_codigo.focus()
    
    def _centralizar_janela(self):
        """ Centraliza a janela na tela. """
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (400 // 2)
        self.janela.geometry(f"450x400+{x}+{y}")
    
    def _carregar_responsaveis(self):
        """ Carrega a lista de responsáveis. """
        
        try:
            responsaveis = self.responsavel_controller.listar_responsaveis()
            
            self.responsaveis_opcoes = []
            self.responsaveis_dict = {}
            
            for resp in responsaveis:
                opcao = f"{resp.get_nome()} - CPF: {resp.get_cpf()}"
                self.responsaveis_opcoes.append(opcao)
                self.responsaveis_dict[opcao] = resp.get_cpf()
            
            if not self.responsaveis_opcoes:
                messagebox.showwarning(
                    "Aviso",
                    "Não há responsáveis cadastrados!\n"
                    "Cadastre pelo menos um responsável antes de cadastrar bombonas."
                )
                if self.janela:
                    self.janela.destroy()
                return False
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar responsáveis:\n{str(e)}")
            if self.janela:
                self.janela.destroy()
            return False
    
    def _criar_formulario(self):
        """ Cria o formulário de cadastro. """
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Cadastro de Bombona", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Campo Código
        ttk.Label(main_frame, text="Código *:").pack(anchor=tk.W)
        self.entry_codigo = ttk.Entry(
            main_frame, 
            textvariable=self.var_codigo, 
            width=30
        )
        self.entry_codigo.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Volume
        ttk.Label(main_frame, text="Volume (Litros) *:").pack(anchor=tk.W)
        self.entry_volume = ttk.Entry(
            main_frame, 
            textvariable=self.var_volume, 
            width=20
        )
        self.entry_volume.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Tipo de Resíduo
        ttk.Label(main_frame, text="Tipo de Resíduo *:").pack(anchor=tk.W)
        
        # Obtém tipos válidos do controller
        try:
            tipos_residuo = self.bombona_controller.get_tipos_residuos_validos()
        except:
            # Fallback - apenas os tipos disponíveis no sistema
            tipos_residuo = ["QUÍMICO", "BIOLÓGICO"]
            
        self.combo_tipo_residuo = ttk.Combobox(
            main_frame,
            textvariable=self.var_tipo_residuo,
            values=tipos_residuo,
            state="readonly",
            width=27
        )
        self.combo_tipo_residuo.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Responsável
        ttk.Label(main_frame, text="Responsável *:").pack(anchor=tk.W)
        self.combo_responsavel = ttk.Combobox(
            main_frame,
            textvariable=self.var_responsavel,
            values=self.responsaveis_opcoes,
            state="readonly",
            width=35
        )
        self.combo_responsavel.pack(anchor=tk.W, pady=(0, 20))
        
        # Observação sobre campos obrigatórios
        ttk.Label(
            main_frame, 
            text="* Campos obrigatórios",
            foreground="red"
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(anchor=tk.W)
        
        # Botão Cadastrar
        self.btn_cadastrar = ttk.Button(
            button_frame,
            text="Cadastrar",
            command=self._cadastrar_bombona,
            width=15,
        )
        self.btn_cadastrar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Limpar
        self.btn_limpar = ttk.Button(
            button_frame,
            text="Limpar",
            command=self._limpar_formulario,
            width=15
        )
        self.btn_limpar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Cancelar
        self.btn_cancelar = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.janela.destroy,
            width=15
        )
        self.btn_cancelar.pack(side=tk.LEFT)
        
        # Enter para cadastrar
        self.janela.bind('<Return>', lambda _: self._cadastrar_bombona())
        self.janela.bind('<Escape>', lambda _: self.janela.destroy())
    
    def _validar_formulario(self):
        """ Valida o formulário antes do cadastro. """
        
        if not self.var_codigo.get().strip():
            messagebox.showerror("Erro", "Código é obrigatório!")
            self.entry_codigo.focus()
            return False
        
        if not self.var_volume.get().strip():
            messagebox.showerror("Erro", "Volume é obrigatório!")
            self.entry_volume.focus()
            return False
        
        try:
            volume = float(self.var_volume.get().replace(',', '.'))
            if volume <= 0:
                messagebox.showerror("Erro", "Volume deve ser maior que zero!")
                self.entry_volume.focus()
                return False
        except ValueError:
            messagebox.showerror("Erro", "Volume deve ser um número válido!")
            self.entry_volume.focus()
            return False
        
        if not self.var_tipo_residuo.get().strip():
            messagebox.showerror("Erro", "Tipo de resíduo é obrigatório!")
            self.combo_tipo_residuo.focus()
            return False
        
        if not self.var_responsavel.get().strip():
            messagebox.showerror("Erro", "Responsável é obrigatório!")
            self.combo_responsavel.focus()
            return False
        
        return True
    
    def _cadastrar_bombona(self):
        """ Cadastra a bombona. """
        
        if not self._validar_formulario():
            return
        
        try:
            # Desabilita o botão durante o processo
            self.btn_cadastrar.config(state='disabled')
            
            # Obtém o CPF do responsável selecionado
            responsavel_selecionado = self.var_responsavel.get()
            cpf_responsavel = self.responsaveis_dict.get(responsavel_selecionado)
            
            if not cpf_responsavel:
                messagebox.showerror("Erro", "Responsável selecionado é inválido!")
                return
            
            # Converte volume
            volume = float(self.var_volume.get().replace(',', '.'))
            
            # Chama o controller para cadastrar
            sucesso = self.bombona_controller.cadastrar_bombona(
                self.var_codigo.get().strip(),
                volume,
                self.var_tipo_residuo.get().strip(),
                cpf_responsavel
            )
            
            if sucesso:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Bombona '{self.var_codigo.get().strip()}' cadastrada com sucesso!"
                )
                
                # Pergunta se quer cadastrar outra
                resposta = messagebox.askyesno(
                    "Cadastrar Outra", 
                    "Deseja cadastrar outra bombona?"
                )
                
                if resposta:
                    self._limpar_formulario()
                else:
                    # Verifica se janela existe antes de destruir
                    if hasattr(self, 'janela') and self.janela.winfo_exists():
                        self.janela.destroy()
                    return  # Sai da função para não tentar reabilitar botão
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar bombona:\n{str(e)}")
        
        finally:
            # Só reabilita botão se widget ainda existir
            try:
                if hasattr(self, 'btn_cadastrar') and hasattr(self, 'janela'):
                    if self.janela.winfo_exists():
                        self.btn_cadastrar.config(state='normal')
            except tk.TclError:
                # Widget foi destruído - não faz nada
                pass
    
    def _limpar_formulario(self):
        """ Limpa todos os campos do formulário. """
        self.var_codigo.set("")
        self.var_volume.set("")
        self.var_tipo_residuo.set("")
        self.var_responsavel.set("")
        
        # Foca no primeiro campo
        self.entry_codigo.focus()
