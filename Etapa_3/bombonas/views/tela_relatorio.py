"""
Tela de relatórios - Versão Simples e Intuitiva
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class TelaRelatorio:
    """
    Tela simples para gerar relatórios do sistema com seleção única de formato.
    """

    def __init__(self, parent):
        """ Inicializa a tela de relatórios. """
        self.parent = parent
        self.janela = None
        
        # Importa seus controllers
        from controllers.bombona_controller import BombonaController
        from controllers.responsavel_controller import ResponsavelController
        
        # Cria objetos dos controllers
        self.bombona_controller = BombonaController()
        self.responsavel_controller = ResponsavelController()
        
        # Variáveis usadas na classe
        self.var_formato_arquivo = tk.StringVar()
        self.var_filtro_setor = tk.StringVar()
        self.var_filtro_responsavel = tk.StringVar()
        self.var_filtro_tipo_residuo = tk.StringVar()
        
        # Dados para filtros
        self.responsaveis_dict = {}
        self.setores_disponiveis = []
        self.tipos_residuo_disponiveis = []
    
    def exibir_tela(self):
        """ Exibe a tela de relatórios. """
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Relatórios do Sistema")
        self.janela.geometry("650x800")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Carrega dados para filtros
        self._carregar_dados_filtros()
        
        # Cria a interface
        self._criar_interface()
    
    def _centralizar_janela(self):
        """ Centraliza a janela na tela. """
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (475 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (625 // 2)
        self.janela.geometry(f"475x625+{x}+{y}")
    
    def _carregar_dados_filtros(self):
        """ Carrega os dados necessários para os filtros. """
        try:
            # Carrega responsáveis
            responsaveis = self.responsavel_controller.listar_responsaveis()
            self.responsaveis_dict = {}
            setores = set()
            
            for resp in responsaveis:
                opcao = f"{resp.get_nome()} - {resp.get_cpf()}"
                self.responsaveis_dict[opcao] = resp.get_cpf()
                setores.add(resp.get_setor())
            
            self.setores_disponiveis = sorted(list(setores))
            
            # Carrega tipos de resíduo
            try:
                self.tipos_residuo_disponiveis = self.bombona_controller.get_tipos_residuos_validos()
            except:
                self.tipos_residuo_disponiveis = ["QUÍMICO", "BIOLÓGICO"]
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
            self.janela.focus()
    
    def _criar_interface(self):
        """ Cria a interface da tela de relatórios. """
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Relatórios do Sistema", font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Seção de formato de arquivo
        self._criar_selecao_formato(main_frame)
        
        # Seção de filtros
        self._criar_filtros(main_frame)
        
        # Seção de relatórios completos
        self._criar_relatorios_completos(main_frame)
        
        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.janela.destroy, width=15).pack(pady=(20, 0))
    
    def _criar_selecao_formato(self, parent):
        """ Cria a seção de seleção do formato de arquivo. """
        
        formato_frame = ttk.LabelFrame(parent, text="Formato do Arquivo", padding="15")
        formato_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(formato_frame, text="Selecione o formato para todos os relatórios:", 
                 font=('Arial', 10)).pack(anchor=tk.W, pady=(0, 5))
        
        combo_formato = ttk.Combobox(
            formato_frame,
            textvariable=self.var_formato_arquivo,
            values=["CSV", "PDF"],  # Opções: .csv e .pdf
            state="readonly",
            width=15
        )
        combo_formato.set("CSV")
        combo_formato.pack(anchor=tk.W)
    
    def _criar_filtros(self, parent):
        """ Cria a seção de filtros. """
        
        filtros_frame = ttk.LabelFrame(parent, text="Relatório com Filtros", padding="15")
        filtros_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Filtro por Setor
        ttk.Label(filtros_frame, text="Setor:").pack(anchor=tk.W)
        combo_setor = ttk.Combobox(
            filtros_frame,
            textvariable=self.var_filtro_setor,
            values=["Todos"] + self.setores_disponiveis,
            state="readonly",
            width=30
        )
        combo_setor.set("Todos")
        combo_setor.pack(anchor=tk.W, pady=(0, 8))
        
        # Filtro por Responsável
        ttk.Label(filtros_frame, text="Responsável:").pack(anchor=tk.W)
        combo_resp = ttk.Combobox(
            filtros_frame,
            textvariable=self.var_filtro_responsavel,
            values=["Todos"] + list(self.responsaveis_dict.keys()),
            state="readonly",
            width=30
        )
        combo_resp.set("Todos")
        combo_resp.pack(anchor=tk.W, pady=(0, 8))
        
        # Filtro por Tipo de Resíduo
        ttk.Label(filtros_frame, text="Tipo de Resíduo:").pack(anchor=tk.W)
        combo_tipo = ttk.Combobox(
            filtros_frame,
            textvariable=self.var_filtro_tipo_residuo,
            values=["Todos"] + self.tipos_residuo_disponiveis,
            state="readonly",
            width=30
        )
        combo_tipo.set("Todos")
        combo_tipo.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame para botões
        botoes_frame = ttk.Frame(filtros_frame)
        botoes_frame.pack(fill=tk.X)
        
        # Botão baixar
        ttk.Button(botoes_frame, text="Baixar", command=self._baixar_filtrado, 
                  width=15).pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão limpar filtros
        ttk.Button(botoes_frame, text="Limpar Filtros", command=self._limpar_filtros, 
                  width=15).pack(side=tk.LEFT)
    
    def _criar_relatorios_completos(self, parent):
        """ Cria a seção de relatórios completos. """
        
        completos_frame = ttk.LabelFrame(parent, text="Relatórios Completos", padding="15")
        completos_frame.pack(fill=tk.X)
        
        ttk.Label(completos_frame, text="Selecione o tipo de relatório completo:", 
                 font=('Arial', 10)).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para botões lado a lado
        botoes_frame = ttk.Frame(completos_frame)
        botoes_frame.pack()
        
        ttk.Button(botoes_frame, text="Bombonas", command=self._baixar_bombonas_completo, 
                  width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_frame, text="Responsáveis", command=self._baixar_responsaveis_completo, 
                  width=20).pack(side=tk.LEFT)
    
    def _limpar_filtros(self):
        """ Limpa todos os filtros. """
        self.var_filtro_setor.set("Todos")
        self.var_filtro_responsavel.set("Todos")
        self.var_filtro_tipo_residuo.set("Todos")
    
    def _aplicar_filtros(self, bombonas):
        """ Aplica os filtros às bombonas usando os métodos do controller. """
        
        try:
            # Lista de filtros a aplicar
            filtros = []
            
            # Coleta filtros ativos
            if self.var_filtro_setor.get() != "Todos":
                filtros.append(('setor', self.var_filtro_setor.get()))
                
            if self.var_filtro_responsavel.get() != "Todos":
                cpf = self.responsaveis_dict.get(self.var_filtro_responsavel.get())
                if cpf:
                    filtros.append(('responsavel', cpf))
                    
            if self.var_filtro_tipo_residuo.get() != "Todos":
                filtros.append(('tipo_residuo', self.var_filtro_tipo_residuo.get()))
            
            # Se não há filtros, retorna lista original
            if not filtros:
                return bombonas
            
            # Aplica filtros usando métodos do controller
            bombonas_resultado = None
            
            for tipo_filtro, valor in filtros:
                if tipo_filtro == 'setor':
                    bombonas_resultado = self.bombona_controller.filtrar_bombonas_por_setor(valor)
                elif tipo_filtro == 'responsavel':
                    if bombonas_resultado is None:
                        bombonas_resultado = self.bombona_controller.buscar_bombonas_por_cpf_responsavel(valor)
                    else:
                        # Aplica sobre resultado anterior
                        bombonas_resultado = [b for b in bombonas_resultado 
                                            if b.get_responsavel() and b.get_responsavel().get_cpf() == valor]
                elif tipo_filtro == 'tipo_residuo':
                    if bombonas_resultado is None:
                        bombonas_resultado = self.bombona_controller.filtrar_bombonas_por_tipo_residuo(valor)
                    else:
                        # Aplica sobre resultado anterior
                        bombonas_resultado = [b for b in bombonas_resultado 
                                            if b.get_tipo_residuo() == valor]
            
            return bombonas_resultado or []
            
        except Exception as e:
            print(f"Erro ao aplicar filtros: {e}")
            self.janela.focus()

            return []
    
    def _verificar_filtros_ativos(self):
        """ Verifica se há filtros ativos. """
        filtros_ativos = []
        
        if self.var_filtro_setor.get() != "Todos":
            filtros_ativos.append(f"Setor: {self.var_filtro_setor.get()}")
        
        if self.var_filtro_responsavel.get() != "Todos":
            filtros_ativos.append(f"Responsável: {self.var_filtro_responsavel.get()}")
        
        if self.var_filtro_tipo_residuo.get() != "Todos":
            filtros_ativos.append(f"Tipo: {self.var_filtro_tipo_residuo.get()}")
        
        return filtros_ativos
    
    def _baixar_filtrado(self):
        """ Baixa relatório com filtros aplicados. """
        try:
            # Verifica se há filtros ativos
            filtros_ativos = self._verificar_filtros_ativos()
            if not filtros_ativos:
                messagebox.showwarning("Aviso", "Aplique pelo menos um filtro antes de baixar.")
                self.janela.focus()
                return
            
            # Aplica filtros
            bombonas = self.bombona_controller.listar_bombonas()
            bombonas_filtradas = self._aplicar_filtros(bombonas)
            
            if not bombonas_filtradas:
                messagebox.showwarning("Aviso", "Nenhuma bombona encontrada com os filtros aplicados.")
                self.janela.focus()

                return
            
            # Gera arquivo
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_bombonas(bombonas_filtradas, filtros_ativos, formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório filtrado:\n{str(e)}")
            self.janela.focus()
    
    def _baixar_bombonas_completo(self):
        """ Baixa relatório completo de bombonas. """
        try:
            bombonas = self.bombona_controller.listar_bombonas()
            if not bombonas:
                messagebox.showwarning("Aviso", "Nenhuma bombona cadastrada.")
                self.janela.focus()

                return
            
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_bombonas(bombonas, [], formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório de bombonas:\n{str(e)}")
            self.janela.focus()
    
    def _baixar_responsaveis_completo(self):
        """ Baixa relatório completo de responsáveis. """
        try:
            responsaveis = self.responsavel_controller.listar_responsaveis()
            if not responsaveis:
                messagebox.showwarning("Aviso", "Nenhum responsável cadastrado.")
                return
            
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_responsaveis(responsaveis, formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório de responsáveis:\n{str(e)}")
            self.janela.focus()

    def _gerar_arquivo_bombonas(self, bombonas, filtros_ativos, formato):
        """ Solicita geração de arquivo ao controller. """
        
        # View só escolhe onde salvar
        if formato == "csv":
            filetypes = [("CSV files", "*.csv"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        else:
            filetypes = [("PDF files", "*.pdf"), ("CSV files", "*.csv"), ("All files", "*.*")]
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=f".{formato}",
            filetypes=filetypes
        )
        
        if not arquivo:
            return
        
        try:
            arquivo_gerado = self.bombona_controller.gerar_relatorio(
                bombonas_filtradas=bombonas,
                arquivo=arquivo,
                filtros_ativos=filtros_ativos,
                formato=formato
            )
            
            messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\n\nLocal: {arquivo_gerado}")
            self.janela.focus()
            
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                import os
                os.startfile(arquivo_gerado)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
            self.janela.focus()
    
    def _gerar_arquivo_responsaveis(self, responsaveis, formato):
        """ Solicita geração de arquivo de responsáveis ao controller. """
        
        # View só escolhe onde salvar
        if formato == "csv":
            filetypes = [("CSV files", "*.csv"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        else:
            filetypes = [("PDF files", "*.pdf"), ("CSV files", "*.csv"), ("All files", "*.*")]
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=f".{formato}",
            filetypes=filetypes
        )
        
        if not arquivo:
            return
        
        try:
            arquivo_gerado = self.responsavel_controller.gerar_relatorio(
                responsaveis=responsaveis,
                arquivo=arquivo,
                formato=formato
            )
            
            messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\n\nLocal: {arquivo_gerado}")
            self.janela.focus()
            
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                import os
                os.startfile(arquivo_gerado)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
            self.janela.focus()
    