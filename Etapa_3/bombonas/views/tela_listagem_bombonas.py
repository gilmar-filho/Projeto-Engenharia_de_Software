"""
Tela de listagem de bombonas - Versão Simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TelaListagemBombonas:
    """
    Tela simplificada para listar e gerenciar bombonas.
    """
    
    def __init__(self, parent, bombona_controller, responsavel_controller):
        """
        Inicializa a tela de listagem.
        
        Args:
            parent: Janela pai
            bombona_controller: Controller de bombonas
            responsavel_controller: Controller de responsáveis
        """
        self.parent = parent
        self.bombona_controller = bombona_controller
        self.responsavel_controller = responsavel_controller
        self.janela = None
        self.tree = None
    
    def exibir_lista(self):
        """Exibe a tela de listagem."""
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Lista de Bombonas")
        self.janela.geometry("900x500")
        self.janela.resizable(True, True)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Cria a interface
        self._criar_interface()
        
        # Carrega os dados
        self._carregar_bombonas()
    
    def _centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (500 // 2)
        self.janela.geometry(f"900x500+{x}+{y}")
    
    def _criar_interface(self):
        """Cria a interface da listagem."""
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame, 
            text="Lista de Bombonas", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 10))
        
        # Frame da tabela
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Criação da Treeview
        colunas = ('Código', 'Volume', 'Tipo Resíduo', 'Responsável', 'CPF')
        self.tree = ttk.Treeview(table_frame, columns=colunas, show='headings', height=15)
        
        # Configuração das colunas
        self.tree.heading('Código', text='Código')
        self.tree.heading('Volume', text='Volume (L)')
        self.tree.heading('Tipo Resíduo', text='Tipo de Resíduo')
        self.tree.heading('Responsável', text='Responsável')
        self.tree.heading('CPF', text='CPF')
        
        # Largura das colunas ajustadas para caber na janela (900px de largura)
        self.tree.column('Código', width=100, anchor=tk.CENTER)
        self.tree.column('Volume', width=80, anchor=tk.CENTER)
        self.tree.column('Tipo Resíduo', width=120, anchor=tk.CENTER)
        self.tree.column('Responsável', width=200, anchor=tk.W)
        self.tree.column('CPF', width=130, anchor=tk.CENTER)
        
        # APENAS scrollbar vertical
        scrollbar_v = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_v.set)
        
        # Pack da tabela e scrollbar vertical apenas
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para duplo clique
        self.tree.bind('<Double-1>', self._on_duplo_clique)
        
        # Frame dos botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Botões da esquerda
        ttk.Button(
            button_frame,
            text="Editar",
            command=self._editar_bombona,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="Excluir",
            command=self._excluir_bombona,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão da direita
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.janela.destroy,
            width=15
        ).pack(side=tk.RIGHT)
        
        # Bind para teclas
        self.janela.bind('<Delete>', lambda e: self._excluir_bombona())
    
    def _carregar_bombonas(self):
        """Carrega a lista de bombonas."""
        
        try:
            # Limpa a tabela
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Busca as bombonas
            bombonas = self.bombona_controller.listar_bombonas()
            # print(bombonas)
            
            # Popula a tabela
            for bombona in bombonas:
                responsavel = bombona.get_responsavel()
                
                if responsavel:
                    nome_resp = responsavel.get_nome()
                    cpf_resp = responsavel.get_cpf()
                else:
                    nome_resp = "N/A"
                    cpf_resp = "N/A"
                
                # Insere na tabela
                self.tree.insert('', tk.END, values=(
                    bombona.get_codigo(),
                    f"{bombona.get_volume():.1f}",
                    bombona.get_tipo_residuo(),
                    nome_resp,
                    cpf_resp
                ))
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar bombonas:\n{str(e)}")
    
    def _obter_bombona_selecionada(self):
        """Obtém a bombona selecionada na tabela."""
        
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma bombona na lista.")
            return None
        
        # Pega os valores da linha selecionada
        item = self.tree.item(selecao[0])
        valores = item['values']
        
        if not valores:
            return None
        
        # O código está na primeira coluna
        codigo = valores[0]
        
        # Busca a bombona completa
        bombonas = self.bombona_controller.listar_bombonas()
        for bombona in bombonas:
            if bombona.get_codigo() == codigo:
                return bombona
        
        return None
    
    def _on_duplo_clique(self, event):
        """Ação de duplo clique na tabela."""
        self._editar_bombona()
    
    def _editar_bombona(self):
        """Edita a bombona selecionada."""
        
        bombona = self._obter_bombona_selecionada()
        if not bombona:
            return
        
        # Abre janela de edição
        self._abrir_janela_edicao(bombona)
    
    def _abrir_janela_edicao(self, bombona):
        """Abre janela para edição da bombona."""
        
        # Cria nova janela
        janela_edicao = tk.Toplevel(self.janela)
        janela_edicao.title("Editar Bombona")
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
            text="Editar Bombona", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Variáveis dos campos
        var_volume = tk.StringVar(value=str(bombona.get_volume()))
        var_tipo_residuo = tk.StringVar(value=bombona.get_tipo_residuo())
        var_responsavel = tk.StringVar()
        
        # Campo Código (apenas informativo)
        ttk.Label(main_frame, text="Código da Bombona:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(
            main_frame, 
            text=bombona.get_codigo(),
            font=('Arial', 10),
            foreground="blue"
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Campo Volume
        ttk.Label(main_frame, text="Volume (Litros) *:").pack(anchor=tk.W)
        entry_volume = ttk.Entry(
            main_frame, 
            textvariable=var_volume, 
            width=20
        )
        entry_volume.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Tipo de Resíduo
        ttk.Label(main_frame, text="Tipo de Resíduo *:").pack(anchor=tk.W)
        
        # Obtém tipos válidos do controller
        try:
            tipos_residuo = self.bombona_controller.get_tipos_residuos_validos()
        except:
            tipos_residuo = ["Químico", "Biológico"]
            
        combo_tipo_residuo = ttk.Combobox(
            main_frame,
            textvariable=var_tipo_residuo,
            values=tipos_residuo,
            state="readonly",
            width=27
        )
        combo_tipo_residuo.pack(anchor=tk.W, pady=(0, 10))
        
        # Campo Responsável
        ttk.Label(main_frame, text="Responsável *:").pack(anchor=tk.W)
        
        # Carrega responsáveis
        try:
            responsaveis = self.responsavel_controller.listar_responsaveis()
            
            responsaveis_opcoes = []
            responsaveis_dict = {}
            responsavel_atual = None
            
            for resp in responsaveis:
                opcao = f"{resp.get_nome()} - CPF: {resp.get_cpf()}"
                responsaveis_opcoes.append(opcao)
                responsaveis_dict[opcao] = resp.get_cpf()
                
                # Verifica se é o responsável atual
                if bombona.get_responsavel() and resp.get_cpf() == bombona.get_responsavel().get_cpf():
                    responsavel_atual = opcao
            
            # Se não encontrou responsável atual, adiciona opção "Responsável Atual"
            if not responsavel_atual and bombona.get_responsavel():
                resp_atual = bombona.get_responsavel()
                responsavel_atual = f"{resp_atual.get_nome()} - CPF: {resp_atual.get_cpf()}"
                responsaveis_opcoes.insert(0, responsavel_atual)
                responsaveis_dict[responsavel_atual] = resp_atual.get_cpf()
            
            var_responsavel.set(responsavel_atual if responsavel_atual else "")
            
        except Exception as e:
            responsaveis_opcoes = []
            responsaveis_dict = {}
            messagebox.showerror("Erro", f"Erro ao carregar responsáveis: {e}")
        
        combo_responsavel = ttk.Combobox(
            main_frame,
            textvariable=var_responsavel,
            values=responsaveis_opcoes,
            state="readonly",
            width=35
        )
        combo_responsavel.pack(anchor=tk.W, pady=(0, 20))
        
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
            if not var_volume.get().strip():
                messagebox.showerror("Erro", "Volume é obrigatório!")
                entry_volume.focus()
                return
            
            try:
                volume = float(var_volume.get().replace(',', '.'))
                if volume <= 0:
                    messagebox.showerror("Erro", "Volume deve ser maior que zero!")
                    entry_volume.focus()
                    return
            except ValueError:
                messagebox.showerror("Erro", "Volume deve ser um número válido!")
                entry_volume.focus()
                return
            
            if not var_tipo_residuo.get().strip():
                messagebox.showerror("Erro", "Tipo de resíduo é obrigatório!")
                combo_tipo_residuo.focus()
                return
            
            if not var_responsavel.get().strip():
                messagebox.showerror("Erro", "Responsável é obrigatório!")
                combo_responsavel.focus()
                return
            
            try:
                # Obtém o CPF do responsável selecionado
                responsavel_selecionado = var_responsavel.get()
                cpf_responsavel = responsaveis_dict.get(responsavel_selecionado)
                
                if not cpf_responsavel:
                    messagebox.showerror("Erro", "Responsável selecionado é inválido!")
                    return
                
                # Chama o controller para editar
                sucesso = self.bombona_controller.editar_bombona(
                    bombona.get_codigo(),  # Código original da bombona
                    volume,
                    var_tipo_residuo.get().strip(),
                    cpf_responsavel
                )
                
                if sucesso:
                    messagebox.showinfo("Sucesso", "Bombona editada com sucesso!")
                    janela_edicao.destroy()
                    # Recarrega a lista
                    self._carregar_bombonas()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao editar bombona:\n{str(e)}")
        
        # Função para limpar campos (exceto código)
        def limpar_campos():
            var_volume.set("")
            var_tipo_residuo.set("")
            var_responsavel.set("")
            entry_volume.focus()
        
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
        entry_volume.focus()
        
        # Configurar Enter para salvar
        janela_edicao.bind('<Return>', lambda e: salvar_edicao())
        janela_edicao.bind('<Escape>', lambda e: janela_edicao.destroy())
    
    def _excluir_bombona(self):
        """Exclui a bombona selecionada."""
        
        bombona = self._obter_bombona_selecionada()
        if not bombona:
            return
        
        # Confirma a exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a bombona?\n\n"
            f"Código: {bombona.get_codigo()}\n"
            f"Volume: {bombona.get_volume()} L\n"
            f"Tipo: {bombona.get_tipo_residuo()}\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if not resposta:
            return
        
        try:
            # Tenta remover a bombona
            sucesso = self.bombona_controller.remover_bombona(bombona.get_codigo())
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Bombona excluída com sucesso!")
                # Recarrega a lista
                self._carregar_bombonas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir bombona:\n{str(e)}")