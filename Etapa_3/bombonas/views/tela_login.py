"""
Tela de login ultra simplificada
"""

import tkinter as tk
from tkinter import ttk, messagebox


class TelaLogin:
    def __init__(self, callback_sucesso, login="admin", senha="123456"):
        self.callback_sucesso = callback_sucesso
        self.login_correto = login
        self.senha_correta = senha
    
    def exibir_login(self):
        # Cria janela
        self.janela = tk.Tk()
        self.janela.title("Login - Sistema de Bombonas")
        self.janela.geometry("300x300")
        self.janela.resizable(False, False)
        
        # Centraliza
        x = (self.janela.winfo_screenwidth() // 2) - 300
        y = (self.janela.winfo_screenheight() // 2) - 300
        self.janela.geometry(f"300x300+{x}+{y}")
        
        # Interface
        frame = ttk.Frame(self.janela, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Sistema de Bombonas", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Campos
        ttk.Label(frame, text="Login:").pack()
        self.entry_login = ttk.Entry(frame, width=20)
        self.entry_login.pack(pady=(0, 10))
        
        ttk.Label(frame, text="Senha:").pack()
        self.entry_senha = ttk.Entry(frame, width=20, show="*")
        self.entry_senha.pack(pady=(0, 15))
        
        # Botões
        ttk.Button(frame, text="Entrar", command=self._login, width=15).pack(pady=(30, 10))
        ttk.Button(frame, text="Sair", command=self._sair, width=15).pack()
        
        # Eventos
        self.janela.bind('<Return>', lambda e: self._login())
        self.janela.bind('<Escape>', lambda e: self._sair())
        self.janela.protocol("WM_DELETE_WINDOW", self._sair)
        
        self.entry_login.focus()
        self.janela.mainloop()
    
    def _login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        if login == self.login_correto and senha == self.senha_correta:
            self.janela.destroy()
            self.callback_sucesso()
        else:
            messagebox.showerror("Erro", f"Credenciais incorretas!\nUse: {self.login_correto}/{self.senha_correta}")
            self.entry_senha.delete(0, tk.END)
            self.entry_login.focus()
    
    def _sair(self):
        if messagebox.askyesno("Sair", "Deseja sair?"):
            self.janela.destroy()
            exit()