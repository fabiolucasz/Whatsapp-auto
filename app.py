import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import webbrowser
import time
import bcrypt

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        # Conectar ao banco de dados e criar a tabela se não existir
        self.criar_tabela()

        # Label e Entry para o usuário
        self.label_usuario = tk.Label(root, text="Usuário:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack()

        # Label e Entry para a senha
        self.label_senha = tk.Label(root, text="Senha:")
        self.label_senha.pack()
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.pack()

        # Botão para fazer login
        self.botao_login = tk.Button(root, text="Login", command=self.verificar_login)
        self.botao_login.pack()

        # Botão para registrar
        self.botao_registrar = tk.Button(root, text="Registrar", command=self.abrir_registro)
        self.botao_registrar.pack()

    def criar_tabela(self):
        # Conexão com o banco de dados
        conexao = sqlite3.connect('cadastro.db')
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                senha TEXT
            )
        """)
        conexao.commit()
        cursor.close()
        conexao.close()

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Verifica as credenciais no banco de dados
        if self.verificar_credenciais(usuario, senha):
            self.root.destroy()  # Fecha a janela de login
            self.abrir_whatsapp()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas")

    def verificar_credenciais(self, usuario, senha):
        # Conexão com o banco de dados
        conexao = sqlite3.connect('cadastro.db')

        # Verifica as credenciais no banco de dados
        cursor = conexao.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario=?", (usuario,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()

        if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8')):
            return True
        else:
            return False

    def abrir_registro(self):
        self.root.withdraw()  # Oculta a janela de login
        self.registro_janela = tk.Toplevel(self.root)
        self.registro_janela.title("Registrar")
        self.registro_janela.geometry("300x200")

        # Label e Entry para o usuário
        self.label_usuario_reg = tk.Label(self.registro_janela, text="Usuário:")
        self.label_usuario_reg.pack()
        self.entry_usuario_reg = tk.Entry(self.registro_janela)
        self.entry_usuario_reg.pack()

        # Label e Entry para a senha
        self.label_senha_reg = tk.Label(self.registro_janela, text="Senha:")
        self.label_senha_reg.pack()
        self.entry_senha_reg = tk.Entry(self.registro_janela, show="*")
        self.entry_senha_reg.pack()

        # Botão para salvar o registro
        self.botao_salvar_reg = tk.Button(self.registro_janela, text="Salvar", command=self.salvar_registro)
        self.botao_salvar_reg.pack()

        # Botão para voltar ao login
        self.botao_voltar_login = tk.Button(self.registro_janela, text="Voltar ao Login", command=self.voltar_login)
        self.botao_voltar_login.pack()

    def salvar_registro(self):
        usuario = self.entry_usuario_reg.get()
        senha = self.entry_senha_reg.get()

        # Hash da senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        # Conexão com o banco de dados
        conexao = sqlite3.connect('cadastro.db')

        cursor = conexao.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hashed_senha.decode('utf-8')))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Registro salvo com sucesso")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro ao salvar registro: {e}")
        finally:
            cursor.close()
            conexao.close()

    def voltar_login(self):
        self.registro_janela.destroy()
        self.root.deiconify()

    def abrir_whatsapp(self):
        root = tk.Tk()
        app = WhatsappAuto(root)
        root.mainloop()

class WhatsappAuto:
    def __init__(self, root):
        self.root = root
        self.root.title("Whatsapp Auto")

        # Cria um estilo ttk para os botões
        estilo = ttk.Style()
        estilo.configure("Botao.TButton", font=('Helvetica', 10))
        estilo.map("Botao.TButton", foreground=[('pressed', 'black'), ('active', 'white')])

        # Texto para inserir mensagens com quebras de linha
        self.numero = tk.Text(root, height=1, width=14)
        self.numero.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Texto para inserir mensagens com quebras de linha
        self.texto_mensagem = tk.Text(root, height=5, width=30)
        self.texto_mensagem.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        # Botão para iniciar o WebBrowser Chrome
        self.botao_iniciar_webbrowser = tk.Button(root, text="Mensagens personalizadas", command=self.iniciar_webbrowser)
        self.botao_iniciar_webbrowser.grid(row=12, column=1, padx=10, pady=10, sticky='we')

    def iniciar_webbrowser(self):
        # Número de telefone do contato (no formato internacional, sem espaços ou caracteres especiais)
        numero_contato = self.numero.get("1.0", "end").strip()
        print(numero_contato)

        # Mensagem que será enviada
        mensagem = self.texto_mensagem.get("1.0", "end").strip()
        print(mensagem)

        # Construímos o link com o número do contato e a mensagem
        link_whatsapp = f"https://web.whatsapp.com/send?phone={numero_contato}&text={mensagem}"

        # Abrimos o link no navegador padrão do sistema
        webbrowser.open(link_whatsapp)

        # Tempo para o WhatsApp ser carregado
        time.sleep(20)  # Ajuste conforme necessário

        # Você pode adicionar um tempo extra para esperar o carregamento completo da página, se necessário

        # Fecha o navegador (opcional)
        #pyautogui.hotkey('ctrl', 'w')  # Fecha a aba do navegador

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginApp(root)
    root.mainloop()
