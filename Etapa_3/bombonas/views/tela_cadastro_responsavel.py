"""
Tela de cadastro de responsável - Versão Simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TelaCadastroResponsavel:
    """
    Tela simplificada para cadastrar novos responsáveis.
    """
    
    def __init__(self, parent):
        """ Inicializa a tela de cadastro. """
        self.parent = parent
        self.janela = None
        
        # Cria seu controller
        from controllers.responsavel_controller import ResponsavelController
        self.responsavel_controller = ResponsavelController()
        
        # Variáveis dos campos
        self.var_cpf = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_telefone = tk.StringVar()
        self.var_setor = tk.StringVar()
    
    def exibir_formulario(self):
        """ Exibe a tela de cadastro. """
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Cadastro de Responsável")
        self.janela.geometry("450x400")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Cria o formulário
        self._criar_formulario()
        
        # Foca no primeiro campo
        self.entry_cpf.focus()
    
    def _centralizar_janela(self):
        """ Centraliza a janela na tela. """
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (400 // 2)
        self.janela.geometry(f"450x400+{x}+{y}")
    
    def _criar_formulario(self):
        """ Cria o formulário de cadastro. """
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Cadastro de Responsável", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Campo CPF
        ttk.Label(main_frame, text="CPF *:").pack(anchor=tk.W)
        self.entry_cpf = ttk.Entry(
            main_frame, 
            textvariable=self.var_cpf, 
            width=30
        )
        self.entry_cpf.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Nome
        ttk.Label(main_frame, text="Nome Completo *:").pack(anchor=tk.W)
        self.entry_nome = ttk.Entry(
            main_frame, 
            textvariable=self.var_nome, 
            width=40
        )
        self.entry_nome.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Telefone
        ttk.Label(main_frame, text="Telefone *:").pack(anchor=tk.W)
        self.entry_telefone = ttk.Entry(
            main_frame, 
            textvariable=self.var_telefone, 
            width=30
        )
        self.entry_telefone.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Setor
        ttk.Label(main_frame, text="Setor *:").pack(anchor=tk.W)
        self.entry_setor = ttk.Entry(
            main_frame, 
            textvariable=self.var_setor, 
            width=30
        )
        self.entry_setor.pack(anchor=tk.W, pady=(0, 20))
        
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
            command=self._cadastrar_responsavel,
            width=15
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
        
        # Configurar Enter para cadastrar
        self.janela.bind('<Return>', lambda _: self._cadastrar_responsavel())
        self.janela.bind('<Escape>', lambda _: self.janela.destroy())
    
    def _validar_formulario(self):
        """ Valida o formulário antes do cadastro. """
        
        if not self.var_cpf.get().strip():
            messagebox.showerror("Erro", "CPF é obrigatório!")
            self.entry_cpf.focus()
            return False
        
        if not self.var_nome.get().strip():
            messagebox.showerror("Erro", "Nome é obrigatório!")
            self.entry_nome.focus()
            return False
        
        if not self.var_telefone.get().strip():
            messagebox.showerror("Erro", "Telefone é obrigatório!")
            self.entry_telefone.focus()
            return False
        
        if not self.var_setor.get().strip():
            messagebox.showerror("Erro", "Setor é obrigatório!")
            self.entry_setor.focus()
            return False
        
        return True
    
    def _cadastrar_responsavel(self):
        """ Cadastra o responsável. """
        
        if not self._validar_formulario():
            return
        
        try:
            # Desabilita o botão durante o processo
            self.btn_cadastrar.config(state='disabled')
            
            # Chama o controller para cadastrar
            sucesso = self.responsavel_controller.cadastrar_responsavel(
                self.var_cpf.get().strip(),
                self.var_nome.get().strip(),
                self.var_telefone.get().strip(),
                self.var_setor.get().strip()
            )
            
            if sucesso:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Responsável '{self.var_nome.get().strip()}' cadastrado com sucesso!"
                )
                
                # Pergunta se quer cadastrar outro
                resposta = messagebox.askyesno(
                    "Cadastrar Outro", 
                    "Deseja cadastrar outro responsável?"
                )
                
                if resposta:
                    self._limpar_formulario()
                else:
                    # Verifica se janela existe antes de destruir
                    if hasattr(self, 'janela') and self.janela.winfo_exists():
                        self.janela.destroy()
                    return  # Sai da função para não tentar reabilitar botão
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar responsável:\n{str(e)}")
            self.janela.focus()
        
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
        self.var_cpf.set("")
        self.var_nome.set("")
        self.var_telefone.set("")
        self.var_setor.set("")
        
        # Foca no primeiro campo
        self.entry_cpf.focus()
    