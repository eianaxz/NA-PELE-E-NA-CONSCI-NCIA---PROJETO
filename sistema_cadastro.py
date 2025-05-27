import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3
from menu import MenuApp  # Importando o sistema de menu

load_dotenv('cadastro.env')


class SistemaCadastro:
    def __init__(self, root):
        self.root = root
        self.db = sqlite3.connect('usuarios.db')
        self.menu_system = None
        self.tentativas_login = 0

        # Configurações de email
        self.EMAIL_SENDER = os.getenv("EMAIL_SENDER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

        if not all([self.EMAIL_SENDER, self.EMAIL_PASSWORD, self.SMTP_SERVER]):
            messagebox.showerror("Erro de Configuração",
                                 "Variáveis de ambiente não configuradas corretamente!")
            exit()

        # Configuração do banco de dados
        self.criar_banco_dados()

        # Configurar interface
        self.setup_interface()

    def criar_banco_dados(self):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                apelido TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def setup_interface(self):
        """Configura a interface gráfica do sistema de cadastro/login"""
        self.root.title("Na Pele e na Consciência - Acess Painel")
        self.root.geometry("800x400")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.root.attributes("-alpha", 0.9)

        try:
            caminho_arquivo = os.path.join(
                os.path.dirname(__file__), "logo.ico")
            self.root.iconbitmap(caminho_arquivo)
        except:
            pass

        # Frames principais
        self.LeftFrame = tk.Frame(
            self.root, width=300, height=800, bg="#100720", relief="raise")
        # Use fill=tk.Y para preencher verticalmente
        self.LeftFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.MiddleFrame = tk.Frame(self.root, width=5, bg="white")
        self.MiddleFrame.pack(side=tk.LEFT, fill=tk.Y)


        self.RightFrame = tk.Frame(
            self.root, width=495, height=400, bg="#100720", relief="raise")
        # Use fill=tk.BOTH e expand=True para preencher todo o espaço restante
        self.RightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Lado Esquerdo
        
        self.logo = tk.PhotoImage(
                file="imagem.png")
        tk.Label(self.LeftFrame, image=self.logo,
                     bg="#100720").place(x=1, y=1)
        

        tk.Label(self.LeftFrame, text="NA PELE E NA CONSCIÊNCIA", font=(
            "Delon", 16), bg="#100720", fg="white").place(x=20, y=350)
        tk.Label(self.LeftFrame, text="-UM SIMULADOR DE DILEMAS ÉTICOS-",
                 font=("Delon", 10), bg="#100720", fg="white").place(x=40, y=375)

        # Criar frames para cada tela
        self.cadastro_frame = tk.Frame(self.RightFrame, bg="#100720")
        self.login_frame = tk.Frame(self.RightFrame, bg="#100720")

        # Configurar a tela de cadastro
        self.setup_cadastro_screen()
        # Configurar a tela de login
        self.setup_login_screen()

        # Mostrar tela de cadastro inicialmente
        self.mostrar_cadastro()

        # Mostrar critérios do nome assim que a janela é aberta
        self.root.after(100, lambda: self.instruir("nome"))

    def setup_cadastro_screen(self):
        """Configura os widgets da tela de cadastro dentro do cadastro_frame"""
        tk.Label(self.cadastro_frame, text="CADASTRO DO USUÁRIO", font=(
            "Times New Roman", 20), bg="#100720", fg="white").place(x=70, y=20)
        tk.Label(self.cadastro_frame, text="🧠 Quem está entrando na simulação?", font=(
            "Times New Roman", 14), bg="#100720", fg="white").place(x=70, y=70)

        # Campo Nome
        self.NomeLabel = tk.Label(self.cadastro_frame, text="Nome:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.NomeLabel.place(x=70, y=110)
        self.NomeEntry = ttk.Entry(self.cadastro_frame, width=30)
        self.NomeEntry.place(x=130, y=110)

        # Campo Apelido
        self.ApelidotLabel = tk.Label(self.cadastro_frame, text="🪪 Como você gostaria de ser chamado (a)?", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.ApelidoLabel = tk.Label(self.cadastro_frame, text="Apelido:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.ApelidoEntry = ttk.Entry(self.cadastro_frame, width=28)

        # Campo Email
        self.EmailtLabel = tk.Label(self.cadastro_frame, text="📧 Seu melhor email: ", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.EmailLabel = tk.Label(self.cadastro_frame, text="Email:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.EmailEntry = ttk.Entry(self.cadastro_frame, width=30)

        # Campo Senha
        self.SenhatLabel = tk.Label(self.cadastro_frame, text="🔒 Crie uma Senha", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.SenhaLabel = tk.Label(self.cadastro_frame, text="Senha:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.SenhaEntry = ttk.Entry(self.cadastro_frame, width=30, show="*")

        # Campo Confirmar Senha
        self.ConfirmarLabel = tk.Label(self.cadastro_frame, text="Confirme sua senha:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.ConfirmarEntry = ttk.Entry(
            self.cadastro_frame, width=30, show="*")

        # Checkbox para mostrar senha
        self.mostrar_senha = tk.Checkbutton(self.cadastro_frame, text="Mostrar Senha", bg="#100720", fg="white",
                                            activebackground="#100720", activeforeground="white",
                                            command=self.alternar_senha)

        # Botões
        self.CadastrarButton = ttk.Button(
            self.cadastro_frame, text="Cadastrar", width=20, command=self.cadastrar_usuario)
        self.CadastrarButton.place(x=120, y=370)
        self.LoginButton = ttk.Button(
            self.cadastro_frame, text="Login", width=20, command=self.mostrar_login)
        self.LoginButton.place(x=260, y=370)

        # Configurar eventos
        self.NomeEntry.bind("<Return>", self.handle_nome)
        self.ApelidoEntry.bind("<Return>", self.handle_apelido)
        self.EmailEntry.bind("<Return>", self.handle_email)
        self.SenhaEntry.bind("<Return>", self.handle_senha)
        self.ConfirmarEntry.bind(
            "<Return>", lambda e: self.cadastrar_usuario())

    def setup_login_screen(self):
        """Configura os widgets da tela de login dentro do login_frame"""
        tk.Label(self.login_frame, text="LOGIN DO USUÁRIO", font=(
            "Times New Roman", 20), bg="#100720", fg="white").place(x=130, y=20)
        tk.Label(self.login_frame, text="🧾 Bem vindo (a) de volta!", font=(
            "Times New Roman", 14), bg="#100720", fg="white").place(x=160, y=60)

        # Email
        tk.Label(self.login_frame, text="📧 Email:", font=(
            "Times New Roman", 14), bg="#100720", fg="white").place(x=70, y=110)
        self.email_login = ttk.Entry(self.login_frame, width=30)
        self.email_login.place(x=160, y=110)

        # Senha
        self.senha_label = tk.Label(self.login_frame, text="🔒 Senha:", font=(
            "Times New Roman", 14), bg="#100720", fg="white")
        self.senha_entry = ttk.Entry(self.login_frame, width=30, show="*")
        self.mostrar_senha_login = tk.Checkbutton(self.login_frame, text="Mostrar Senha", bg="#100720", fg="white",
                                                  activebackground="#100720", activeforeground="white",
                                                  command=self.alternar_senha_login)

        # Botões
        self.login_button = ttk.Button(
            self.login_frame, text="Entrar", command=self.verificar_login)
        self.esqueceu_senha_button = ttk.Button(
            self.login_frame, text="Esqueceu a senha?", command=self.redefinir_senha_login)

        # Botão de voltar para cadastro
        ttk.Button(self.login_frame, text="Voltar para Cadastro",
                   command=lambda: [self.mostrar_cadastro(), self.email_login.delete(0, tk.END)]).place(x=180, y=250)

        self.email_login.bind(
            "<Return>", lambda e: self.verificar_email_login())

    # ==============================================
    # FUNÇÕES DE VALIDAÇÃO
    # ==============================================

    def validar_nome(self, nome):
        nome_sem_espacos = nome.replace(" ", "")
        return (nome and
                len(nome_sem_espacos) <= 20 and
                nome_sem_espacos.isalpha())

    def validar_apelido(self, apelido):
        return apelido and len(apelido) <= 10 and " " not in apelido

    def validar_email(self, email):
        if not email or " " in email or "@" not in email:
            return False
        try:
            local_part, domain = email.split("@")
            if not local_part:
                return False
            if not (domain == "gmail.com" or domain == "ufrpe.br"):
                return False
            if not re.match(r"^[a-zA-Z0-9._-]+$", local_part):
                return False
            return True
        except ValueError:
            return False

    def validar_senha(self, senha):
        return (senha and
                len(senha.replace(" ", "")) == 6 and
                " " not in senha)

    # ==============================================
    # FUNÇÕES DE BANCO DE DADOS
    # ==============================================

    def verificar_email_existente(self, email):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None

    def verificar_apelido_existente(self, apelido):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE apelido = ?', (apelido,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None

    def salvar_usuario(self):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios (nome, apelido, email, senha)
                VALUES (?, ?, ?, ?)
            ''', (
                self.NomeEntry.get().strip(),
                self.ApelidoEntry.get().strip(),
                self.EmailEntry.get().strip(),
                self.SenhaEntry.get().strip()
            ))
            conn.commit()
        except sqlite3.IntegrityError as e:
            messagebox.showerror(
                "Erro", f"Erro ao cadastrar usuário: {str(e)}")
        finally:
            conn.close()

    def verificar_credenciais(self, email, senha):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None

    def obter_senha_atual(self, email):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT senha FROM usuarios WHERE email = ?', (email,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

    # ==============================================
    # FUNÇÕES DE 2FA (AUTENTICAÇÃO EM DUAS ETAPAS)
    # ==============================================

    def gerar_codigo(self):
        return str(random.randint(100000, 999999))

    def enviar_codigo_email(self, destinatario, codigo):
        try:
            msg = MIMEText(
                f"Olá! Seja bem vindo (a) ao Na Pele e na Consciência\n Seu código de verificação é: {codigo}\n\nEste código é válido por 5 minutos.")
            msg['Subject'] = 'Código de Verificação - Na Pele e na Consciência'
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = destinatario

            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                server.sendmail(self.EMAIL_SENDER,
                                destinatario, msg.as_string())
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False

    def verificar_codigo(self):
        codigo_digitado = self.codigo_entry.get()
        if not codigo_digitado.isdigit() or len(codigo_digitado) != 6:
            messagebox.showerror(
                "Erro", "Código inválido. Deve conter 6 dígitos.")
            return

        if datetime.now() > self.janela_2fa.codigo_valido_ate:
            messagebox.showerror("Erro", "Código expirado. Solicite um novo.")
            return

        if codigo_digitado == self.janela_2fa.codigo_2fa:
            try:
                # Salvar usuário no banco de dados
                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO usuarios (nome, apelido, email, senha)
                    VALUES (?, ?, ?, ?)
                ''', (
                    self.NomeEntry.get().strip(),
                    self.ApelidoEntry.get().strip(),
                    self.EmailEntry.get().strip(),
                    self.SenhaEntry.get().strip()
                ))
                conn.commit()

                # Obter os dados do usuário recém-cadastrado
                cursor.execute('SELECT * FROM usuarios WHERE email = ?',
                               (self.EmailEntry.get().strip(),))
                user = cursor.fetchone()
                conn.close()

                if user:
                    user_data = {
                        "nome": user[1],
                        "apelido": user[2],
                        "email": user[3]
                    }
                    messagebox.showinfo(
                        "Sucesso", "Cadastro concluído com sucesso!")
                    self.janela_2fa.destroy()
                    # Iniciar o menu com os dados do usuário
                    self.iniciar_menu(user_data)
            except sqlite3.IntegrityError as e:
                messagebox.showerror(
                    "Erro", f"Falha ao cadastrar usuário: {str(e)}")
                self.janela_2fa.destroy()
        else:
            messagebox.showerror("Erro", "Código incorreto. Tente novamente.")

    def solicitar_novo_codigo(self):
        novo_codigo = self.gerar_codigo()
        self.janela_2fa.codigo_2fa = novo_codigo
        self.janela_2fa.codigo_valido_ate = datetime.now() + timedelta(minutes=5)
        if self.enviar_codigo_email(self.EmailEntry.get().strip(), novo_codigo):
            messagebox.showinfo(
                "Sucesso", "Novo código enviado para seu email!")
        else:
            messagebox.showerror(
                "Erro", "Falha ao enviar novo código. Tente novamente.")

    def criar_janela_2fa(self):
        self.janela_2fa = tk.Toplevel(self.root)
        self.janela_2fa.title("Autenticação em Duas Etapas")
        self.janela_2fa.geometry("400x250")
        self.janela_2fa.resizable(False, False)
        self.janela_2fa.configure(bg="#100720")

        codigo = self.gerar_codigo()
        self.janela_2fa.codigo_2fa = codigo
        self.janela_2fa.codigo_valido_ate = datetime.now() + timedelta(minutes=5)

        if not self.enviar_codigo_email(self.EmailEntry.get().strip(), codigo):
            messagebox.showerror(
                "Erro", "Falha ao enviar código de verificação. Tente novamente.")
            self.janela_2fa.destroy()
            return

        tk.Label(self.janela_2fa, text="🔒 Autenticação em Duas Etapas", font=("Times New Roman", 16),
                 bg="#100720", fg="white").pack(pady=10)

        tk.Label(self.janela_2fa, text="Enviamos um código de 6 dígitos para seu email.",
                 font=("Times New Roman", 12), bg="#100720", fg="white").pack(pady=5)

        tk.Label(self.janela_2fa, text="Digite o código abaixo:",
                 font=("Times New Roman", 12), bg="#100720", fg="white").pack(pady=5)

        self.codigo_entry = ttk.Entry(self.janela_2fa, width=10,
                                      font=("Arial", 14), justify="center")
        self.codigo_entry.pack(pady=7)
        self.codigo_entry.focus_set()

        ttk.Button(self.janela_2fa, text="Verificar",
                   command=self.verificar_codigo).pack(pady=3)

        ttk.Button(self.janela_2fa, text="Enviar novo código",
                   command=self.solicitar_novo_codigo).pack(pady=5)

        tk.Label(self.janela_2fa, text="O código é válido por 5 minutos.",
                 font=("Times New Roman", 10), bg="#100720", fg="white").pack(pady=5, padx=50)

    # ==============================================
    # FUNÇÕES DE REDEFINIÇÃO DE SENHA
    # ==============================================

    def redefinir_senha(self, email):
        def alternar_visibilidade_senha():
            nova_senha_entry.config(
                show="" if nova_senha_entry.cget("show") == "*" else "*")
            confirmar_senha_entry.config(
                show="" if confirmar_senha_entry.cget("show") == "*" else "*")

        def confirmar_redefinicao():
            nova_senha = nova_senha_entry.get().strip()
            confirmar_nova_senha = confirmar_senha_entry.get().strip()

            if not self.validar_senha(nova_senha):
                messagebox.showerror(
                    "Erro", "Senha inválida. Deve ter exatamente 6 caracteres sem espaços.")
                return

            if nova_senha != confirmar_nova_senha:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return

            # Verificar se a nova senha é igual à senha atual
            senha_atual = self.obter_senha_atual(email)
            if nova_senha == senha_atual:
                messagebox.showinfo(
                    "Informação", "Esta senha já está em uso. Por favor, escolha uma nova senha.")
                return

            codigo = self.gerar_codigo()
            janela_redefinicao.codigo_2fa = codigo
            janela_redefinicao.codigo_valido_ate = datetime.now() + timedelta(minutes=5)

            if self.enviar_codigo_email(email, codigo):
                nova_senha_label.pack_forget()
                nova_senha_entry.pack_forget()
                confirmar_senha_label.pack_forget()
                confirmar_senha_entry.pack_forget()
                mostrar_senha_redefinir.pack_forget()
                confirmar_button.pack_forget()

                tk.Label(janela_redefinicao, text="Digite o código de verificação:",
                         font=("Times New Roman", 12), bg="#100720", fg="white").pack(pady=5)
                codigo_entry = ttk.Entry(
                    janela_redefinicao, width=10, font=("Arial", 14), justify="center")
                codigo_entry.pack(pady=10)

                def verificar_codigo_redefinicao():
                    if codigo_entry.get() == janela_redefinicao.codigo_2fa:
                        if datetime.now() > janela_redefinicao.codigo_valido_ate:
                            messagebox.showerror("Erro", "Código expirado.")
                            return

                        conn = sqlite3.connect('usuarios.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            'UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha, email))
                        conn.commit()
                        conn.close()

                        messagebox.showinfo(
                            "Sucesso", "Senha redefinida com sucesso!")
                        janela_redefinicao.destroy()
                        self.realizar_login(email, nova_senha)
                    else:
                        messagebox.showerror("Erro", "Código incorreto.")

                ttk.Button(janela_redefinicao, text="Verificar",
                           command=verificar_codigo_redefinicao).pack(pady=5)
            else:
                messagebox.showerror(
                    "Erro", "Falha ao enviar código de verificação.")

        janela_redefinicao = tk.Toplevel(self.root)
        janela_redefinicao.title("Redefinir Senha")
        janela_redefinicao.geometry("400x350")
        janela_redefinicao.resizable(False, False)
        janela_redefinicao.configure(bg="#100720")

        tk.Label(janela_redefinicao, text="🔑 Redefinir Senha", font=("Times New Roman", 16),
                 bg="#100720", fg="white").pack(pady=10)

        nova_senha_label = tk.Label(janela_redefinicao, text="Nova Senha:", font=("Times New Roman", 12),
                                    bg="#100720", fg="white")
        nova_senha_label.pack(pady=5)

        nova_senha_entry = ttk.Entry(janela_redefinicao, width=30, show="*")
        nova_senha_entry.pack(pady=5)

        confirmar_senha_label = tk.Label(janela_redefinicao, text="Confirmar Nova Senha:",
                                         font=("Times New Roman", 12), bg="#100720", fg="white")
        confirmar_senha_label.pack(pady=5)

        confirmar_senha_entry = ttk.Entry(
            janela_redefinicao, width=30, show="*")
        confirmar_senha_entry.pack(pady=5)

        mostrar_senha_redefinir = tk.Checkbutton(janela_redefinicao, text="Mostrar Senha",
                                                 bg="#100720", fg="white",
                                                 activebackground="#100720",
                                                 activeforeground="white",
                                                 command=alternar_visibilidade_senha)
        mostrar_senha_redefinir.pack(pady=5)

        confirmar_button = ttk.Button(janela_redefinicao, text="Confirmar",
                                      command=confirmar_redefinicao)
        confirmar_button.pack(pady=10)

    def redefinir_senha_login(self):
        """Inicia o processo de redefinição de senha"""
        email = self.email_login.get().strip()
        if not email:
            messagebox.showerror(
                "Erro", "Por favor, insira seu email primeiro.")
            return

        self.redefinir_senha(email)

    # ==============================================
    # FUNÇÕES DE NAVEGAÇÃO ENTRE TELAS
    # ==============================================

    def mostrar_cadastro(self):
        """Mostra a tela de cadastro e oculta a tela de login"""
        self.login_frame.pack_forget()  # Oculta o frame de login
        # Exibe o frame de cadastro
        self.cadastro_frame.pack(fill=tk.BOTH, expand=True)

        # Limpar campos
        self.NomeEntry.delete(0, tk.END)
        self.ApelidoEntry.delete(0, tk.END)
        self.EmailEntry.delete(0, tk.END)
        self.SenhaEntry.delete(0, tk.END)
        self.ConfirmarEntry.delete(0, tk.END)
        self.NomeEntry.focus_set()  # Define o foco para o primeiro campo
         # Exibe as instruções para o campo nome

    def mostrar_login(self):
        """Mostra a tela de login e oculta a tela de cadastro"""
        self.tentativas_login = 0  # Resetar tentativas ao abrir a tela de login
        self.cadastro_frame.pack_forget()  # Oculta o frame de cadastro
        # Exibe o frame de login
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Limpar campos de login e definir foco
        self.email_login.delete(0, tk.END)
        self.senha_entry.delete(0, tk.END)
        self.email_login.focus_set()

        # Ocultar campos de senha até que o email seja validado
        self.senha_label.place_forget()
        self.senha_entry.place_forget()
        self.mostrar_senha_login.place_forget()
        self.login_button.place_forget()
        self.esqueceu_senha_button.place_forget()

    # ==============================================
    # FUNÇÕES AUXILIARES
    # ==============================================

    def instruir(self, campo):
        mensagens = {
            "nome": "Nome:\n • Até 20 caracteres (sem contar espaços)\n • Somente letras e espaços\n • Sem números ou símbolos",
            "apelido": "Apelido:\n • Até 10 caracteres\n • Pode conter letras\n • Pode conter números e símbolos\n • Não pode conter espaços",
            "email": "Email:\n • Domínios válidos: @gmail.com e @ufrpe.br\n • Deve conter @\n • Não pode conter espaços",
            "senha": "Senha:\n • Ter exatamente 6 caracteres (sem espaços)\n • Pode conter letras, números e símbolos\n • Não pode conter espaços",
            "confirmar": "Confirme a senha:\n • Deve ser exatamente igual à senha anterior."
        }
        messagebox.showinfo("Critérios", mensagens[campo])

    def alternar_senha(self):
        self.SenhaEntry.config(
            show="" if self.SenhaEntry.cget("show") == "*" else "*")

    def alternar_senha_login(self):
        self.senha_entry.config(
            show="" if self.senha_entry.cget("show") == "*" else "*")

    def gerar_sugestoes_apelido(self, apelido_base):
        sugestoes = []
        for i in range(1, 4):
            sugestoes.append(f"{apelido_base}{i}")
        return sugestoes

    # ==============================================
    # FUNÇÕES DE MANIPULAÇÃO DE EVENTOS
    # ==============================================

    def handle_nome(self, event):
        nome = self.NomeEntry.get().strip()
        nome_sem_espacos = nome.replace(" ", "")

        if not nome_sem_espacos.isalpha():
            messagebox.showerror(
                "Erro", "Nome inválido. Deve conter apenas letras e espaços.")
            return

        if len(nome_sem_espacos) > 20:
            messagebox.showerror(
                "Erro", f"Nome inválido. Máximo de 20 caracteres (sem espaços). Você digitou {len(nome_sem_espacos)} caracteres.")
            return

        if self.validar_nome(nome):
            self.ApelidotLabel.place(x=70, y=140)
            self.ApelidoLabel.place(x=70, y=170)
            self.ApelidoEntry.place(x=140, y=170)
            self.ApelidoEntry.focus_set()
            self.instruir("apelido")
        else:
            messagebox.showerror("Erro", "Nome inválido.")

    def handle_apelido(self, event):
        apelido = self.ApelidoEntry.get().strip()

        if not self.validar_apelido(apelido):
            messagebox.showerror(
                "Erro", "Apelido inválido. Deve ter até 10 caracteres e não pode conter espaços.")
            return

        if self.verificar_apelido_existente(apelido):
            sugestoes = self.gerar_sugestoes_apelido(apelido)
            mensagem = f"Apelido '{apelido}' já existe. Sugestões:\n\n" + \
                "\n".join(sugestoes)
            messagebox.showinfo("Apelido não disponível", mensagem)
            return

        if self.validar_apelido(apelido):
            self.EmailtLabel.place(x=70, y=210)
            self.EmailLabel.place(x=70, y=240)
            self.EmailEntry.place(x=130, y=240)
            self.EmailEntry.focus_set()
            self.instruir("email")
        else:
            messagebox.showerror("Erro", "Apelido inválido.")

    def handle_email(self, event):
        email = self.EmailEntry.get().strip()
        if not self.validar_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return

        if self.verificar_email_existente(email):
            messagebox.showinfo(
                "Informação", "Este email já está cadastrado. Por favor, realize o login.")
            self.mostrar_login()
            return

        self.SenhatLabel.place(x=70, y=280)
        self.SenhaLabel.place(x=70, y=310)
        self.SenhaEntry.place(x=130, y=310)
        self.mostrar_senha.place(x=270, y=310)
        self.SenhaEntry.focus_set()
        self.instruir("senha")

    def handle_senha(self, event):
        senha = self.SenhaEntry.get().strip()

        if " " in senha:
            messagebox.showerror(
                "Erro", "Senha inválida. Não pode conter espaços.")
            return

        if not self.validar_senha(senha):
            messagebox.showerror(
                "Erro", f"Senha inválida. Deve ter exatamente 6 caracteres (sem espaços). Você digitou {len(senha)} caracteres.")
            return

        if self.validar_senha(senha):
            self.ConfirmarLabel.place(x=70, y=340)
            self.ConfirmarEntry.place(x=230, y=340)
            self.ConfirmarEntry.focus_set()
            self.instruir("confirmar")
        else:
            messagebox.showerror("Erro", "Senha inválida.")

    def cadastrar_usuario(self):
        email = self.EmailEntry.get().strip()
        apelido = self.ApelidoEntry.get().strip()

        if self.verificar_email_existente(email):
            messagebox.showinfo(
                "Informação", "Este email já está cadastrado. Por favor, realize o login.")
            self.mostrar_login()
            return

        if self.verificar_apelido_existente(apelido):
            sugestoes = self.gerar_sugestoes_apelido(apelido)
            mensagem = f"Apelido '{apelido}' já existe. Sugestões:\n\n" + \
                "\n".join(sugestoes)
            messagebox.showinfo("Apelido não disponível", mensagem)
            return

        if (self.validar_nome(self.NomeEntry.get().strip()) and
            self.validar_apelido(apelido) and
            self.validar_email(email) and
            self.validar_senha(self.SenhaEntry.get().strip()) and
                self.SenhaEntry.get().strip() == self.ConfirmarEntry.get().strip()):

            self.criar_janela_2fa()
        else:
            messagebox.showerror(
                "Erro", "As senhas não coincidem.")

    # ==============================================
    # FUNÇÕES DE LOGIN
    # ==============================================

    def verificar_email_login(self):
        """Verifica o email digitado na tela de login"""
        email = self.email_login.get().strip()
        if not self.validar_email(email):
            messagebox.showerror(
                "Erro", "Email inválido. Por favor, insira um email válido.")
            return

        # Verificar se o email existe no banco de dados
        if not self.verificar_email_existente(email):
            messagebox.showinfo("Email não cadastrado",
                                "Este email não está cadastrado. Por favor, insira um email válido ou realize o cadastro.")
            return

        # Se o email existe, mostrar campos de senha
        self.senha_label.place(x=70, y=160)
        self.senha_entry.place(x=160, y=160)
        self.mostrar_senha_login.place(x=300, y=160)
        self.login_button.place(x=200, y=210)
        self.esqueceu_senha_button.place(x=200, y=290)
        self.senha_entry.focus_set()

    def verificar_login(self):
        """Verifica as credenciais de login"""
        email = self.email_login.get().strip()
        senha = self.senha_entry.get().strip()

        if self.verificar_credenciais(email, senha):
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_data = {
                    "nome": user[1],
                    "apelido": user[2],
                    "email": user[3]
                }
                self.iniciar_menu(user_data)
        else:
            self.tentativas_login += 1
            if self.tentativas_login >= 3:
                messagebox.showerror(
                    "Erro", "Você excedeu o número máximo de tentativas. Por favor, redefina sua senha.")
                self.redefinir_senha_login()
                self.tentativas_login = 0
            else:
                messagebox.showerror(
                    "Erro", f"Email ou senha incorretos. Tentativas restantes: {3 - self.tentativas_login}")

    def realizar_login(self, email, senha):
        """Realiza o login do usuário"""
        if self.verificar_credenciais(email, senha):
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_data = {
                    "nome": user[1],
                    "apelido": user[2],
                    "email": user[3]
                }
                self.iniciar_menu(user_data)
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    # ==============================================
    # FUNÇÃO PARA INICIAR O MENU PRINCIPAL
    # ==============================================

    def iniciar_menu(self, user_data):
        """Inicia o sistema de menu com os dados do usuário"""
        # Destruir a janela atual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Iniciar o sistema de menu
        self.menu_system = MenuApp(self.root, self, user_data=user_data)
        self.menu_system.setup_ui()


# Função principal para iniciar o aplicativo


def main():
    root = tk.Tk()
    app = SistemaCadastro(root)
    root.mainloop()


if __name__ == "__main__":
    main()

