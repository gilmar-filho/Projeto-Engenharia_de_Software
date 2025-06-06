"""
Tela de relatórios - Versão Simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


class TelaRelatorio:
    """
    Tela simplificada para gerar relatórios do sistema.
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
    
    def exibir_tela(self):
        """Exibe a tela de relatórios."""
        
        # Cria nova janela
        self.janela = tk.Toplevel(self.parent)
        self.janela.title("Relatórios do Sistema")
        self.janela.geometry("500x400")
        self.janela.resizable(False, False)
        
        # Centraliza a janela
        self._centralizar_janela()
        
        # Cria a interface
        self._criar_interface()
    
    def _centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (400 // 2)
        self.janela.geometry(f"500x400+{x}+{y}")
    
    def _criar_interface(self):
        """Cria a interface da tela de relatórios."""
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            main_frame,
            text="Relatórios do Sistema",
            font=('Arial', 16, 'bold')
        )
        titulo.pack(pady=(0, 20))
        
        # Seção de estatísticas rápidas
        self._criar_estatisticas(main_frame)
        
        # Seção de relatórios
        self._criar_opcoes_relatorios(main_frame)
        
        # Botão fechar
        ttk.Button(
            main_frame,
            text="Fechar",
            command=self.janela.destroy,
            width=15
        ).pack(pady=(20, 0))
    
    def _criar_estatisticas(self, parent):
        """Cria a seção de estatísticas rápidas."""
        
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas Rápidas", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        try:
            # Busca dados para estatísticas
            responsaveis = self.responsavel_controller.listarResponsaveis()
            bombonas = self.bombona_controller.listarBombonas()
            
            total_responsaveis = len(responsaveis)
            total_bombonas = len(bombonas)
            volume_total = sum(b.getVolume() for b in bombonas)
            
            # Exibe estatísticas
            ttk.Label(
                stats_frame,
                text=f"Total de Responsáveis: {total_responsaveis}",
                font=('Arial', 10)
            ).pack(anchor=tk.W, pady=2)
            
            ttk.Label(
                stats_frame,
                text=f"Total de Bombonas: {total_bombonas}",
                font=('Arial', 10)
            ).pack(anchor=tk.W, pady=2)
            
            ttk.Label(
                stats_frame,
                text=f"Volume Total: {volume_total:.1f} L",
                font=('Arial', 10)
            ).pack(anchor=tk.W, pady=2)
            
            if total_bombonas > 0:
                volume_medio = volume_total / total_bombonas
                ttk.Label(
                    stats_frame,
                    text=f"Volume Médio: {volume_medio:.1f} L",
                    font=('Arial', 10)
                ).pack(anchor=tk.W, pady=2)
            
        except Exception as e:
            ttk.Label(
                stats_frame,
                text=f"Erro ao carregar estatísticas: {str(e)}",
                foreground="red"
            ).pack()
    
    def _criar_opcoes_relatorios(self, parent):
        """Cria as opções de relatórios."""
        
        relatorios_frame = ttk.LabelFrame(parent, text="Gerar Relatórios", padding="15")
        relatorios_frame.pack(fill=tk.X)
        
        # Botão para relatório completo
        ttk.Button(
            relatorios_frame,
            text="Relatório Completo (TXT)",
            command=self._gerar_relatorio_txt,
            width=30
        ).pack(pady=5)
        
        ttk.Button(
            relatorios_frame,
            text="Relatório Completo (CSV)",
            command=self._gerar_relatorio_csv,
            width=30
        ).pack(pady=5)
        
        ttk.Button(
            relatorios_frame,
            text="Relatório de Responsáveis",
            command=self._gerar_relatorio_responsaveis,
            width=30
        ).pack(pady=5)
        
        ttk.Button(
            relatorios_frame,
            text="Relatório de Bombonas",
            command=self._gerar_relatorio_bombonas,
            width=30
        ).pack(pady=5)
    
    def _gerar_relatorio_txt(self):
        """Gera relatório completo em formato TXT."""
        
        try:
            # Solicita local para salvar
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Relatório TXT",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not arquivo:
                return
            
            # Chama o controller para gerar o relatório
            arquivo_gerado = self.bombona_controller.gerar_relatorio("txt")
            
            # Copia o arquivo gerado para o local escolhido
            import shutil
            shutil.copy2(arquivo_gerado, arquivo)
            
            messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\n\nLocal: {arquivo}")
            
            # Pergunta se quer abrir o arquivo
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                os.startfile(arquivo)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório:\n{str(e)}")
    
    def _gerar_relatorio_csv(self):
        """Gera relatório completo em formato CSV."""
        
        try:
            # Solicita local para salvar
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Relatório CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not arquivo:
                return
            
            # Gera arquivo CSV manualmente
            self._criar_csv_completo(arquivo)
            
            messagebox.showinfo("Sucesso", f"Relatório CSV salvo com sucesso!\n\nLocal: {arquivo}")
            
            # Pergunta se quer abrir o arquivo
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                os.startfile(arquivo)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório CSV:\n{str(e)}")
    
    def _criar_csv_completo(self, arquivo):
        """Cria um arquivo CSV completo."""
        
        import csv
        
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho do CSV
            writer.writerow(['Tipo', 'Codigo/CPF', 'Nome', 'Volume/Telefone', 'Tipo_Residuo/Setor', 'Responsavel_CPF'])
            
            # Dados dos responsáveis
            responsaveis = self.responsavel_controller.listar_responsaveis()
            for resp in responsaveis:
                writer.writerow(['RESPONSAVEL', resp.get_cpf(), resp.get_nome(), resp.get_telefone(), resp.get_setor(), ''])
            
            # Dados das bombonas
            bombonas = self.bombona_controller.listar_bombonas()
            for bomb in bombonas:
                resp = bomb.get_responsavel()
                cpf_resp = resp.get_cpf() if resp else 'N/A'
                writer.writerow(['BOMBONA', bomb.get_codigo(), '', bomb.get_volume(), bomb.get_tipo_residuo(), cpf_resp])
    
    def _gerar_relatorio_responsaveis(self):
        """Gera relatório específico de responsáveis."""
        
        try:
            # Solicita local para salvar
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Relatório de Responsáveis",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not arquivo:
                return
            
            # Gera relatório de responsáveis
            responsaveis = self.responsavel_controller.listar_responsaveis()
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write("RELATÓRIO DE RESPONSÁVEIS\n")
                f.write("=" * 50 + "\n\n")
                
                for i, resp in enumerate(responsaveis, 1):
                    f.write(f"Responsável {i}:\n")
                    f.write(f"  Nome: {resp.get_nome()}\n")
                    f.write(f"  CPF: {resp.get_cpf()}\n")
                    f.write(f"  Telefone: {resp.get_telefone()}\n")
                    f.write(f"  Setor: {resp.get_setor()}\n\n")
                
                f.write(f"Total de responsáveis: {len(responsaveis)}\n")
            
            messagebox.showinfo("Sucesso", f"Relatório de responsáveis salvo!\n\nLocal: {arquivo}")
            
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                os.startfile(arquivo)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório de responsáveis:\n{str(e)}")
    
    def _gerar_relatorio_bombonas(self):
        """Gera relatório específico de bombonas."""
        
        try:
            # Solicita local para salvar
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Relatório de Bombonas",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not arquivo:
                return
            
            # Gera relatório de bombonas
            bombonas = self.bombona_controller.listar_bombonas()
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write("RELATÓRIO DE BOMBONAS\n")
                f.write("=" * 50 + "\n\n")
                
                volume_total = 0
                for i, bomb in enumerate(bombonas, 1):
                    resp = bomb.get_responsavel()
                    volume_total += bomb.get_volume()
                    
                    f.write(f"Bombona {i}:\n")
                    f.write(f"  Código: {bomb.get_codigo()}\n")
                    f.write(f"  Volume: {bomb.get_volume():.1f} L\n")
                    f.write(f"  Tipo de Resíduo: {bomb.get_tipo_residuo()}\n")
                    f.write(f"  Responsável: {resp.get_nome() if resp else 'N/A'}\n")
                    f.write(f"  CPF Responsável: {resp.get_cpf() if resp else 'N/A'}\n\n")
                
                f.write(f"Total de bombonas: {len(bombonas)}\n")
                f.write(f"Volume total: {volume_total:.1f} L\n")
                if bombonas:
                    f.write(f"Volume médio: {volume_total/len(bombonas):.1f} L\n")
            
            messagebox.showinfo("Sucesso", f"Relatório de bombonas salvo!\n\nLocal: {arquivo}")
            
            if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o relatório agora?"):
                os.startfile(arquivo)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório de bombonas:\n{str(e)}")