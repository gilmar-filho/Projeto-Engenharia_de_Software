"""
Tela de listagem de responsáveis - Versão Simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TelaListagemResponsaveis:
    """
    Tela simplificada para listar e gerenciar responsáveis.
    """

    def __init__(self, parent):
        """
        Inicializa a tela de listagem.
        """
        self.parent = parent
        self.janela = None
        self.tree = None
        
        # Cria seu controller
        from controllers.responsavel_controller import ResponsavelController
        self.responsavel_controller = ResponsavelController()
    
    def exibir_lista(self):
        """ Exibe a tela de listagem. """
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Lista de Responsáveis")
        self.janela.geometry("800x500")
        self.janela.resizable(True, True)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Cria a interface
        self._criar_interface()
        
        # Carrega os dados
        self._carregar_responsaveis()
    
    def _centralizar_janela(self):
        """ Centraliza a janela na tela. """
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (500 // 2)
        self.janela.geometry(f"800x500+{x}+{y}")
    
    def _criar_interface(self):
        """ Cria a interface da listagem. """
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Lista de Responsáveis", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 10))
        
        # Frame da tabela
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Criação da Treeview
        colunas = ('Nome', 'CPF', 'Telefone', 'Setor')
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings', height=15)
        
        # Configuração das colunas
        self.tree.heading('Nome', text='Nome Completo')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Setor', text='Setor')
        
        # Largura das colunas
        self.tree.column('Nome', width=250, anchor=tk.W)
        self.tree.column('CPF', width=120, anchor=tk.CENTER)
        self.tree.column('Telefone', width=120, anchor=tk.CENTER)
        self.tree.column('Setor', width=150, anchor=tk.CENTER)
        
        # Scrollbar vertical apenas
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack da tabela e scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para duplo clique
        self.tree.bind('<Double-1>', lambda _: self._editar_responsavel())
        
        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Botões da esquerda
        ttk.Button(
            button_frame,
            text="Editar",
            command=self._editar_responsavel,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Excluir",
            command=self._excluir_responsavel,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão da direita (apenas Fechar)
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.janela.destroy,
            width=15
        ).pack(side=tk.RIGHT)
        
        # Bind para teclas
        self.janela.bind('<Delete>', lambda _: self._excluir_responsavel())
    
    def _carregar_responsaveis(self):
        """ Carrega a lista de responsáveis. """
        
        try:
            # Limpa a tabela
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Busca os responsáveis
            responsaveis = self.responsavel_controller.listar_responsaveis()
            
            # Popula a tabela
            for responsavel in responsaveis:
                self.tree.insert('', tk.END, values=(
                    responsavel.get_nome(),
                    responsavel.get_cpf(),
                    responsavel.get_telefone(),
                    responsavel.get_setor()
                ))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar responsáveis:\n{str(e)}")
            self.janela.focus()
    
    def _obter_responsavel_selecionado(self):
        """ Obtém o responsável selecionado na tabela. """
        
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um responsável na lista.")
            self.janela.focus()
            return None
        
        # Pega os valores da linha selecionada
        item = self.tree.item(selecao[0])
        valores = item['values']
        
        if not valores:
            return None
        
        # O CPF está na segunda coluna
        cpf = valores[1]
        
        # Busca o responsável completo
        responsavel = self.responsavel_controller.buscar_responsavel(cpf)
        
        return responsavel
        
    def _editar_responsavel(self):
        """ Edita o responsável selecionado. """
        
        responsavel = self._obter_responsavel_selecionado()
        if not responsavel:
            return
        
        # Abre janela de edição
        self._abrir_janela_edicao(responsavel)
    
    def _abrir_janela_edicao(self, responsavel):
        """ Abre janela para edição do responsável. """
        
        # Cria nova janela
        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Responsável")
        janela_edicao.geometry("450x400")
        janela_edicao.resizable(False, False)
        
        # Centraliza a janela
        janela_edicao.update_idletasks()
        x = (janela_edicao.winfo_screenwidth() // 2) - (450 // 2)
        y = (janela_edicao.winfo_screenheight() // 2) - (400 // 2)
        janela_edicao.geometry(f"450x400+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(janela_edicao, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Editar Responsável", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Variáveis dos campos
        cpf_formatado = responsavel.get_cpf()
        var_nome = tk.StringVar(value=responsavel.get_nome())
        var_telefone = tk.StringVar(value=responsavel.get_telefone())
        var_setor = tk.StringVar(value=responsavel.get_setor())
        
        # Campo CPF (apenas informativo)
        ttk.Label(main_frame, text="CPF do Responsável:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(
            main_frame, 
            text=cpf_formatado,
            font=('Arial', 10),
            foreground="blue"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Campo Nome
        ttk.Label(main_frame, text="Nome Completo *:").pack(anchor=tk.W)
        entry_nome = ttk.Entry(
            main_frame, 
            textvariable=var_nome, 
            width=40
        )
        entry_nome.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Telefone
        ttk.Label(main_frame, text="Telefone *:").pack(anchor=tk.W)
        entry_telefone = ttk.Entry(
            main_frame, 
            textvariable=var_telefone, 
            width=30
        )
        entry_telefone.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Setor
        ttk.Label(main_frame, text="Setor *:").pack(anchor=tk.W)
        entry_setor = ttk.Entry(
            main_frame, 
            textvariable=var_setor, 
            width=30
        )
        entry_setor.pack(anchor=tk.W, pady=(0, 20))
        
        # Observação sobre campos obrigatórios
        ttk.Label(
            main_frame, 
            text="* Campos obrigatórios",
            foreground="red"
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(anchor=tk.W)
        
        # Função para salvar as alterações
        def salvar_edicao():
            # Validação básica
            if not var_nome.get().strip():
                messagebox.showerror("Erro", "Nome é obrigatório!")
                entry_nome.focus()
                return
            
            if not var_telefone.get().strip():
                messagebox.showerror("Erro", "Telefone é obrigatório!")
                entry_telefone.focus()
                return
            
            if not var_setor.get().strip():
                messagebox.showerror("Erro", "Setor é obrigatório!")
                entry_setor.focus()
                return
            
            try:
                # Chama o controller para editar (usando CPF original, não formatado)
                sucesso = self.responsavel_controller.editar_responsavel(
                    responsavel.get_cpf(),  # CPF original do objeto
                    var_nome.get().strip(),
                    var_telefone.get().strip(),
                    var_setor.get().strip()
                )
                
                if sucesso:
                    messagebox.showinfo("Sucesso", "Responsável editado com sucesso!")
                    janela_edicao.destroy()
                    # Recarrega a lista
                    self._carregar_responsaveis()
                    self.janela.focus()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar responsável:\n{str(e)}")
                self.janela.focus()
        
        # Função para limpar campos (exceto CPF)
        def limpar_campos():
            var_nome.set("")
            var_telefone.set("")
            var_setor.set("")
            entry_nome.focus()
        
        # Botão Salvar (equivalente ao Cadastrar)
        btn_salvar = ttk.Button(
            button_frame,
            text="Salvar",
            command=salvar_edicao,
            width=15
        )
        btn_salvar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Limpar
        btn_limpar = ttk.Button(
            button_frame,
            text="Limpar",
            command=limpar_campos,
            width=15
        )
        btn_limpar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Cancelar
        btn_cancelar = ttk.Button(
            button_frame,
            text="Cancelar",
            command=janela_edicao.destroy,
            width=15
        )
        btn_cancelar.pack(side=tk.LEFT)
        
        # Foca no primeiro campo editável
        entry_nome.focus()
        
        # Configurar Enter para salvar
        janela_edicao.bind('<Return>', lambda _: salvar_edicao())
        janela_edicao.bind('<Escape>', lambda _: janela_edicao.destroy())
    
    def _excluir_responsavel(self):
        """ Exclui o responsável selecionado. """
        
        responsavel = self._obter_responsavel_selecionado()
        if not responsavel:
            return
        
        # Confirma a exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o responsável?\n\n"
            f"Nome: {responsavel.get_nome()}\n"
            f"CPF: {responsavel.get_cpf()}\n"
            f"Setor: {responsavel.get_setor()}\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if not resposta:
            return
        
        try:
            # Tenta remover o responsável
            sucesso = self.responsavel_controller.remover_responsavel(responsavel.get_cpf())
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Responsável excluído com sucesso!")
                # Recarrega a lista
                self._carregar_responsaveis()
                self.janela.focus()

            
        except Exception as e:
            # O controller já trata casos como responsável com bombonas
            messagebox.showerror("Erro", f"Erro ao excluir responsável:\n{str(e)}")
            self.janela.focus()
