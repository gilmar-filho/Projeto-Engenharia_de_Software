"""
Tela de relatórios - Versão Simples e Intuitiva
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv


class TelaRelatorio:
    """
    Tela simples para gerar relatórios do sistema com seleção única de formato.
    """
    
    def __init__(self, parent, bombona_controller, responsavel_controller):
        """
        Inicializa a tela de relatórios.
        
        Args:
            parent: Janela pai
            bombona_controller: Controller de bombonas
            responsavel_controller: Controller de responsáveis
        """
        self.parent = parent
        self.bombona_controller = bombona_controller
        self.responsavel_controller = responsavel_controller
        self.janela = None
        
        # Variáveis
        self.var_formato_arquivo = tk.StringVar()
        self.var_filtro_setor = tk.StringVar()
        self.var_filtro_responsavel = tk.StringVar()
        self.var_filtro_tipo_residuo = tk.StringVar()
        
        # Dados para filtros
        self.responsaveis_dict = {}
        self.setores_disponiveis = []
        self.tipos_residuo_disponiveis = []
    
    def exibir_tela(self):
        """Exibe a tela de relatórios."""
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Relatórios do Sistema")
        self.janela.geometry("500x650")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Carrega dados para filtros
        self._carregar_dados_filtros()
        
        # Cria a interface
        self._criar_interface()
    
    def _centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (650 // 2)
        self.janela.geometry(f"500x650+{x}+{y}")
    
    def _carregar_dados_filtros(self):
        """Carrega os dados necessários para os filtros."""
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
    
    def _criar_interface(self):
        """Cria a interface da tela de relatórios."""
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Relatórios do Sistema", font=('Arial', 16, 'bold'))
        titulo.pack(pady=(0, 20))
        
        # Seção de estatísticas
        self._criar_estatisticas(main_frame)
        
        # Seção de formato de arquivo
        self._criar_selecao_formato(main_frame)
        
        # Seção de filtros
        self._criar_filtros(main_frame)
        
        # Seção de relatórios completos
        self._criar_relatorios_completos(main_frame)
        
        # Botão fechar
        ttk.Button(main_frame, text="Fechar", command=self.janela.destroy, width=15).pack(pady=(20, 0))
    
    def _criar_estatisticas(self, parent):
        """Cria a seção de estatísticas rápidas."""
        
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        try:
            responsaveis = self.responsavel_controller.listar_responsaveis()
            bombonas = self.bombona_controller.listar_bombonas()
            
            total_responsaveis = len(responsaveis)
            total_bombonas = len(bombonas)
            
            ttk.Label(stats_frame, text=f"Responsáveis: {total_responsaveis}").pack(anchor=tk.W)
            ttk.Label(stats_frame, text=f"Bombonas: {total_bombonas}").pack(anchor=tk.W)
            
        except Exception as e:
            ttk.Label(stats_frame, text=f"Erro: {str(e)}", foreground="red").pack()
    
    def _criar_selecao_formato(self, parent):
        """Cria a seção de seleção do formato de arquivo."""
        
        formato_frame = ttk.LabelFrame(parent, text="Formato do Arquivo", padding="15")
        formato_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(formato_frame, text="Selecione o formato para todos os relatórios:", 
                 font=('Arial', 10)).pack(anchor=tk.W, pady=(0, 5))
        
        combo_formato = ttk.Combobox(
            formato_frame,
            textvariable=self.var_formato_arquivo,
            values=["CSV", "TXT"],
            state="readonly",
            width=15
        )
        combo_formato.set("CSV")
        combo_formato.pack(anchor=tk.W)
    
    def _criar_filtros(self, parent):
        """Cria a seção de filtros."""
        
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
        """Cria a seção de relatórios completos."""
        
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
        """Limpa todos os filtros."""
        self.var_filtro_setor.set("Todos")
        self.var_filtro_responsavel.set("Todos")
        self.var_filtro_tipo_residuo.set("Todos")
    
    def _aplicar_filtros(self, bombonas):
        """Aplica os filtros às bombonas."""
        bombonas_filtradas = bombonas.copy()
        
        # Filtro por setor
        if self.var_filtro_setor.get() != "Todos":
            setor = self.var_filtro_setor.get()
            bombonas_filtradas = [b for b in bombonas_filtradas 
                                 if b.get_responsavel() and b.get_responsavel().get_setor() == setor]
        
        # Filtro por responsável
        if self.var_filtro_responsavel.get() != "Todos":
            cpf = self.responsaveis_dict.get(self.var_filtro_responsavel.get())
            if cpf:
                bombonas_filtradas = [b for b in bombonas_filtradas 
                                     if b.get_responsavel() and b.get_responsavel().get_cpf() == cpf]
        
        # Filtro por tipo de resíduo
        if self.var_filtro_tipo_residuo.get() != "Todos":
            tipo = self.var_filtro_tipo_residuo.get()
            bombonas_filtradas = [b for b in bombonas_filtradas if b.get_tipo_residuo() == tipo]
        
        return bombonas_filtradas
    
    def _verificar_filtros_ativos(self):
        """Verifica se há filtros ativos."""
        filtros_ativos = []
        
        if self.var_filtro_setor.get() != "Todos":
            filtros_ativos.append(f"Setor: {self.var_filtro_setor.get()}")
        
        if self.var_filtro_responsavel.get() != "Todos":
            filtros_ativos.append(f"Responsável: {self.var_filtro_responsavel.get()}")
        
        if self.var_filtro_tipo_residuo.get() != "Todos":
            filtros_ativos.append(f"Tipo: {self.var_filtro_tipo_residuo.get()}")
        
        return filtros_ativos
    
    def _baixar_filtrado(self):
        """Baixa relatório com filtros aplicados."""
        try:
            # Verifica se há filtros ativos
            filtros_ativos = self._verificar_filtros_ativos()
            if not filtros_ativos:
                messagebox.showwarning("Aviso", "Aplique pelo menos um filtro antes de baixar.")
                return
            
            # Aplica filtros
            bombonas = self.bombona_controller.listar_bombonas()
            bombonas_filtradas = self._aplicar_filtros(bombonas)
            
            if not bombonas_filtradas:
                messagebox.showwarning("Aviso", "Nenhuma bombona encontrada com os filtros aplicados.")
                return
            
            # Gera arquivo
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_bombonas(bombonas_filtradas, "Bombonas_Filtradas", filtros_ativos, formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório filtrado:\n{str(e)}")
    
    def _baixar_bombonas_completo(self):
        """Baixa relatório completo de bombonas."""
        try:
            bombonas = self.bombona_controller.listar_bombonas()
            if not bombonas:
                messagebox.showwarning("Aviso", "Nenhuma bombona cadastrada.")
                return
            
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_bombonas(bombonas, "Bombonas_Completo", [], formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório de bombonas:\n{str(e)}")
    
    def _baixar_responsaveis_completo(self):
        """Baixa relatório completo de responsáveis."""
        try:
            responsaveis = self.responsavel_controller.listar_responsaveis()
            if not responsaveis:
                messagebox.showwarning("Aviso", "Nenhum responsável cadastrado.")
                return
            
            formato = self.var_formato_arquivo.get().lower()
            self._gerar_arquivo_responsaveis(responsaveis, "Responsaveis_Completo", formato)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar relatório de responsáveis:\n{str(e)}")
    
    def _gerar_arquivo_bombonas(self, bombonas, nome_base, filtros_ativos, formato):
        """Gera arquivo de bombonas no formato especificado."""
        ext = f".{formato}"
        
        # Define tipos de arquivo baseado no formato selecionado
        if formato == "csv":
            filetypes = [("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        else:
            filetypes = [("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=ext,
            filetypes=filetypes
        )
        
        if not arquivo:
            return
        
        if formato == "csv":
            self._criar_csv_bombonas(arquivo, bombonas, filtros_ativos)
        else:
            self._criar_txt_bombonas(arquivo, bombonas, filtros_ativos)
        
        messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\n\nLocal: {arquivo}")
        
        if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
            os.startfile(arquivo)
    
    def _gerar_arquivo_responsaveis(self, responsaveis, nome_base, formato):
        """Gera arquivo de responsáveis no formato especificado."""
        ext = f".{formato}"
        
        # Define tipos de arquivo baseado no formato selecionado
        if formato == "csv":
            filetypes = [("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        else:
            filetypes = [("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=ext,
            filetypes=filetypes
        )
        
        if not arquivo:
            return
        
        if formato == "csv":
            self._criar_csv_responsaveis(arquivo, responsaveis)
        else:
            self._criar_txt_responsaveis(arquivo, responsaveis)
        
        messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\n\nLocal: {arquivo}")
        
        if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
            os.startfile(arquivo)
    
    def _criar_csv_bombonas(self, arquivo, bombonas, filtros_ativos):
        """Cria arquivo CSV de bombonas."""
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho com filtros se houver
            if filtros_ativos:
                writer.writerow([f'# Filtros aplicados: {"; ".join(filtros_ativos)}'])
                writer.writerow([f'# Total de bombonas encontradas: {len(bombonas)}'])
                writer.writerow([])  # Linha vazia
            
            # Cabeçalho da tabela
            writer.writerow(['Código', 'Volume', 'Tipo', 'Responsável', 'Setor'])
            
            # Dados
            for bombona in bombonas:
                resp = bombona.get_responsavel()
                writer.writerow([
                    bombona.get_codigo(),
                    bombona.get_volume(),
                    bombona.get_tipo_residuo(),
                    resp.get_nome() if resp else 'N/A',
                    resp.get_setor() if resp else 'N/A'
                ])
    
    def _criar_txt_bombonas(self, arquivo, bombonas, filtros_ativos):
        """Cria arquivo TXT de bombonas."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            titulo = "RELATÓRIO DE BOMBONAS FILTRADAS" if filtros_ativos else "RELATÓRIO COMPLETO DE BOMBONAS"
            f.write(f"{titulo}\n")
            f.write("=" * 50 + "\n\n")
            
            if filtros_ativos:
                f.write("Filtros aplicados:\n")
                for filtro in filtros_ativos:
                    f.write(f"  • {filtro}\n")
                f.write("\n")
            
            f.write(f"Total de bombonas: {len(bombonas)}\n\n")
            
            for i, bombona in enumerate(bombonas, 1):
                resp = bombona.get_responsavel()
                f.write(f"Bombona {i}:\n")
                f.write(f"  Código: {bombona.get_codigo()}\n")
                f.write(f"  Volume: {bombona.get_volume():.1f} L\n")
                f.write(f"  Tipo: {bombona.get_tipo_residuo()}\n")
                f.write(f"  Responsável: {resp.get_nome() if resp else 'N/A'}\n")
                f.write(f"  Setor: {resp.get_setor() if resp else 'N/A'}\n")
                f.write("-" * 30 + "\n")
    
    def _criar_csv_responsaveis(self, arquivo, responsaveis):
        """Cria arquivo CSV de responsáveis."""
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Nome', 'CPF', 'Telefone', 'Setor', 'Qtd_Bombonas'])
            
            for resp in responsaveis:
                bombonas = self.bombona_controller.buscar_bombonas_por_cpf_responsavel(resp.get_cpf())
                writer.writerow([
                    resp.get_nome(),
                    resp.get_cpf(),
                    resp.get_telefone(),
                    resp.get_setor(),
                    len(bombonas)
                ])
    
    def _criar_txt_responsaveis(self, arquivo, responsaveis):
        """Cria arquivo TXT de responsáveis."""
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO COMPLETO DE RESPONSÁVEIS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total de responsáveis: {len(responsaveis)}\n\n")
            
            for i, resp in enumerate(responsaveis, 1):
                bombonas = self.bombona_controller.buscar_bombonas_por_cpf_responsavel(resp.get_cpf())
                f.write(f"Responsável {i}:\n")
                f.write(f"  Nome: {resp.get_nome()}\n")
                f.write(f"  CPF: {resp.get_cpf()}\n")
                f.write(f"  Telefone: {resp.get_telefone()}\n")
                f.write(f"  Setor: {resp.get_setor()}\n")
                f.write(f"  Bombonas: {len(bombonas)}\n")
                f.write("-" * 30 + "\n")