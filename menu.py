import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import re
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
from mundo_consciencias import MundoConscienciaElias

load_dotenv('cadastro.env')

class MenuApp:
    def __init__(self, root, sistema_cadastro, user_data):
        self.root = root
        self.sistema_cadastro = sistema_cadastro
        self.user_data = user_data
        self.db = sqlite3.connect('usuarios.db')
        
        # Configurações de email para 2FA
        self.EMAIL_SENDER = os.getenv("EMAIL_SENDER")
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        
        # Configurar janela principal
        self.root.title("Na Pele e na consciência - Menu")
        self.root.geometry("1040x800")
        self.root.configure(bg="#100720")
        self.root.resizable(False, False)
        self.root.attributes("-alpha", 0.9)
        
       
        caminho_arquivo = os.path.join(os.path.dirname(__file__), "logo.ico")
        self.root.iconbitmap(caminho_arquivo)
    
        
        # Carregar imagem de fundo
        
        
        # Frame para seções do menu
        self.menu_frame = tk.Frame(self.root, width=200, height=600, bg="#100720", bd=2, relief="raised")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Frame para conteúdo
        self.content_frame = tk.Frame(self.root, bg="#100720", bd=2, relief="groove")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configurar menu lateral
        self.setup_menu()
        
        # Configurar tela inicial
        self.setup_home_screen()
        
        # Variáveis para controle de estado
        self.current_section = None
        self.editing_field = None
    
    def setup_menu(self):
        """Configura os botões do menu lateral"""
        tk.Label(self.menu_frame, text="Menu", font=("Times New Roman", 18, "bold"), 
                 bg="#100720", fg="white").pack(pady=20)
        
        buttons = [
            ("🌍 Mundos de Consciência", self.show_mundos_consciencia),
            ("👤 Perfil Personalizado", self.show_perfil_personalizado),
            ("⚙️ Configurações de Perfil", self.show_configuracoes_perfil),
            ("ℹ️ Sobre", self.show_sobre),
            ("❓ Ajuda", self.show_ajuda)
        ]
        
        # Configurar estilo para os botões do menu
        style = ttk.Style()
        style.configure('Menu.TButton', font=('Arial', 12), padding=10, 
                        foreground='black', background='white', borderwidth=2, relief="groove")
        style.map('Menu.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])
        
        for text, command in buttons:
            btn = ttk.Button(self.menu_frame, text=text, width=25, command=command, style='Menu.TButton') # Aumentado o width
            btn.pack(pady=7, fill=tk.X) # Adicionado fill=tk.X para preencher a largura
        

    def setup_home_screen(self):
        """Configura a tela inicial do menu"""
        self.clear_content_frame()
        
        # Mensagem de boas-vindas
        welcome_msg = f"✨ Olá, seja bem vindo(a) {self.user_data['apelido']}! ✨"
        tk.Label(self.content_frame, text=welcome_msg, font=("Times New Roman", 24, "bold"), 
                 bg="#100720", fg="white").pack(pady=50)
        
        # Botão Iniciar
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 14, 'bold'), padding=15, 
                        foreground='black', background='white', borderwidth=2, relief="raised")
        style.map('Accent.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])

        ttk.Button(self.content_frame, text="🚀 Iniciar", width=25, 
                   command=self.show_mundos_consciencia, style='Accent.TButton').pack(pady=30)

        # Adicionar alguns elementos visuais de decoração
        tk.Label(self.content_frame, text=" 🎮 Viva histórias. Tome decisões. Encare as consequências.", 
                 font=("Times New Roman", 14, "italic"), bg="#100720", fg="#FFA500").pack(pady=20)
        
        self.current_section = "home"
    
    def clear_content_frame(self):
        """Limpa o frame de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_mundos_consciencia(self):
        if self.current_section == "mundos":
            return
            
        self.clear_content_frame()
        self.current_section = "mundos"

        tk.Label(self.content_frame, text="🌍 Mundos de Consciência", font=("Times New Roman", 22, "bold"), 
             bg="#100720", fg="white").pack(pady=20)

        categorias = [
            ("🤝 Responsabilidade Coletiva", "#3D087B"),
            ("⚖️ Dilemas éticos e Justiça Moral", "#6C00FF"),
            ("💔 Renúncia de Sonhos por Sobrevivência", "#F43B86")
        ]
        
        style = ttk.Style()
        style.configure('Category.TButton', font=('Arial', 11), padding=8, 
                        foreground='black', background='white', borderwidth=2, relief="flat")
        style.map('Category.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])

        for categoria, color in categorias:
            frame = tk.Frame(self.content_frame, bg="#100720", highlightbackground=color, 
                             highlightthickness=3, bd=0, relief="solid")
            frame.pack(pady=12, fill=tk.X, padx=70)
            
            tk.Label(frame, text=categoria, font=("Times New Roman", 15), 
                     bg="#100720", fg="white").pack(side=tk.LEFT, padx=15, pady=5)
            
            # Modificação aqui para chamar a história específica quando clicar em "Acessar"
            if "Dilemas éticos" in categoria:
                btn_command = lambda: self.start_historia_elias()
            else:
                btn_command = lambda: messagebox.showinfo("Em desenvolvimento", "Esta categoria estará disponível em breve!")
            
            ttk.Button(frame, text="Acessar", width=12, style='Category.TButton',
                      command=btn_command).pack(side=tk.RIGHT, padx=15, pady=5)
        
        tk.Label(self.content_frame, text="Escolha um mundo para iniciar sua jornada!", 
                 font=("Times New Roman", 12, "italic"), bg="#100720", fg="#ADD8E6").pack(pady=20)

    def start_historia_elias(self):
        """Inicia a história do Julgamento de Elias"""
        self.clear_content_frame()
        self.mundo_elias = MundoConscienciaElias(root=self.root, user_data=self.user_data, content_frame=self.content_frame, menu_app=self)
        self.mundo_elias.show_story_screen()

    def show_perfil_personalizado(self):
        """Mostra a seção Perfil Personalizado"""
        if self.current_section == "perfil":
            return
            
        self.clear_content_frame()
        self.current_section = "perfil"
        
        tk.Label(self.content_frame, text="👤 Perfil Personalizado", font=("Times New Roman", 22, "bold"), 
                 bg="#100720", fg="white").pack(pady=20)
        
        profile_frame = tk.Frame(self.content_frame, bg="#100720", highlightbackground="#6C00FF", 
                                 highlightthickness=3, bd=0, relief="raised")
        profile_frame.pack(pady=25, padx=80, fill=tk.X)

        # -----------------------------------------------------------
        # MODIFICAÇÃO AQUI: Exibir o perfil personalizado
        # -----------------------------------------------------------
        if self.user_data and self.user_data.get("profile"):
            profile_info = self.user_data["profile"]
            profile_name = profile_info.get("name", "Nome Desconhecido")
            profile_description = profile_info.get("description", "Nenhuma descrição disponível.")

            tk.Label(profile_frame, text=f"Seu Perfil de Consciência: {profile_name}", 
                     font=("Times New Roman", 18, "bold"), bg="#100720", fg="white", wraplength=500).pack(pady=15, padx=20)
            
            tk.Label(profile_frame, text="Descrição:", 
                     font=("Times New Roman", 14, "underline"), bg="#100720", fg="white").pack(pady=(10, 5), padx=20, anchor='w')
            
            tk.Label(profile_frame, text=profile_description, 
                     font=("Times New Roman", 14), bg="#100720", fg="white", justify=tk.LEFT, wraplength=550).pack(pady=(0, 20), padx=20)
        else:
            tk.Label(profile_frame, text="Jogue os 'Mundos de Consciência' para gerar seu perfil personalizado!", 
                     font=("Times New Roman", 14), bg="#100720", fg="white", wraplength=500).pack(pady=30, padx=20)
        # -----------------------------------------------------------
        # FIM DA MODIFICAÇÃO
        # -----------------------------------------------------------
        
    def show_configuracoes_perfil(self):
        """Mostra a seção Configurações de Perfil (CRUD)"""
        if self.current_section == "config":
            return
            
        self.clear_content_frame()
        self.current_section = "config"
        
        tk.Label(self.content_frame, text="⚙️ Configurações de Perfil", font=("Times New Roman", 22, "bold"), 
                 bg="#100720", fg="white").pack(pady=20)
        
        # Obter dados atuais do usuário
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (self.user_data['email'],))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return
        
        # Atualiza self.user_data com todos os dados do usuário, incluindo o ID
        self.user_data = {
            "id": user[0],
            "nome": user[1],
            "apelido": user[2],
            "email": user[3],
            "senha": user[4]
        }
        
        # Campos editáveis
        fields = [
            ("👤 Nome:", "nome", self.user_data["nome"]),
            ("🏷️ Apelido:", "apelido", self.user_data["apelido"]),
            ("📧 Email:", "email", self.user_data["email"]),
            ("🔒 Senha:", "senha", "******")
        ]
        
        self.entry_vars = {}
        self.entries = {}
        
        style = ttk.Style()
        style.configure('Edit.TButton', font=('Arial', 10), padding=6, 
                        foreground='black', background='white', borderwidth=1, relief="raised")
        style.map('Edit.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])
         

        for i, (label, field, value) in enumerate(fields):
            frame = tk.Frame(self.content_frame, bg="#100720", highlightbackground="#3D087B", 
                             highlightthickness=2, bd=0, relief="ridge")
            frame.pack(pady=10, fill=tk.X, padx=60)
            
            tk.Label(frame, text=label, font=("Times New Roman", 13), 
                     bg="#100720", fg="white", width=15).pack(side=tk.LEFT, padx=10)
            
            self.entry_vars[field] = tk.StringVar(value=value)
            
            if field == "senha":
                entry_frame = tk.Frame(frame, bg="#100720")
                entry_frame.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
                
                entry = ttk.Entry(entry_frame, textvariable=self.entry_vars[field], 
                                  width=25, show="*")
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3) # Increased internal padding
                
                
            
           
            
            ttk.Button(frame, text="Alterar", width=12, style='Edit.TButton',
                       command=lambda f=field: self.edit_field(f)).pack(side=tk.RIGHT, padx=10)
        
        # Botão para excluir conta
        delete_frame = tk.Frame(self.content_frame, bg="#100720")
        delete_frame.pack(pady=30)
        
        style.configure('Danger.TButton', font=('Arial', 11, 'bold'), padding=10, 
                        foreground='black', background='white', borderwidth=2, relief="raised")
        style.map('Danger.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])

        ttk.Button(delete_frame, text="🗑️ Excluir Conta", style='Danger.TButton',
                   command=self.confirmar_exclusao_conta).pack()
    
    def toggle_password_visibility(self, entry):
        """Alterna entre mostrar e ocultar senha para um campo específico"""
        current_show = entry.cget('show')
        entry.config(show='' if current_show == '*' else '*')
         
    def edit_field(self, field):
        """Inicia a edição de um campo específico"""
        self.editing_field = field
        current_value = self.entry_vars[field].get()
        
        if field == "nome":
            messagebox.showinfo("Critérios", 
                "Nome:\n• Até 20 caracteres (sem contar espaços)\n• Somente letras e espaços\n• Sem números ou símbolos")
            
            new_value = self.show_input_dialog(f"Alterar {field}", f"Novo {field}:", current_value)
            
            if new_value is not None:
                nome_sem_espacos = new_value.replace(" ", "")
                if not nome_sem_espacos.isalpha() or len(nome_sem_espacos) > 20:
                    messagebox.showerror("Erro", "Nome inválido. Insira seu novo nome novamente.")
                    return
                
                if messagebox.askyesno("Confirmação", "Deseja realmente alterar este campo?"):
                    self.update_user_field(field, new_value)
        
        elif field == "apelido":
            messagebox.showinfo("Critérios", 
                "Apelido:\n• Até 10 caracteres\n• Pode conter letras\n• Pode conter números e símbolos\n• Não pode conter espaços")
            
            new_value = self.show_input_dialog(f"Alterar {field}", f"Novo {field}:", current_value)
            
            if new_value is not None:
                if " " in new_value or len(new_value) > 10:
                    messagebox.showerror("Erro", "Apelido inválido. Insira seu novo apelido novamente.")
                    return
                
                # Verificar se o apelido já existe
                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM usuarios WHERE apelido = ? AND id != ?', 
                               (new_value, self.user_data['id']))
                if cursor.fetchone():
                    sugestoes = [f"{new_value}{i}" for i in range(1, 4)]
                    messagebox.showinfo("Apelido em uso", 
                        f"Este apelido já está em uso. Sugestões:\n\n" + "\n".join(sugestoes))
                    conn.close()
                    return
                conn.close()
                
                if messagebox.askyesno("Confirmação", "Deseja realmente alterar este campo?"):
                    self.update_user_field(field, new_value)
        
        elif field == "email":
            messagebox.showinfo("Critérios", 
                "Email:\n• Domínios válidos: @gmail.com e @ufrpe.br\n• Deve conter @\n• Não pode conter espaços")
            
            new_value = self.show_input_dialog(f"Alterar {field}", f"Novo {field}:", current_value)
            
            if new_value is not None:
                if not self.validar_email(new_value):
                    messagebox.showerror("Erro", "Email inválido. Insira seu novo email novamente.")
                    return
                
                # Verificar se o email já existe
                conn = sqlite3.connect('usuarios.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM usuarios WHERE email = ? AND id != ?', 
                               (new_value, self.user_data['id']))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "Este email já está cadastrado no sistema.")
                    conn.close()
                    return
                conn.close()
                
                if messagebox.askyesno("Confirmação", "Deseja realmente alterar este campo?"):
                    self.update_user_field(field, new_value)
        
        elif field == "senha":
            self.change_password()
    
    def validar_email(self, email):
        """Valida o formato do email"""
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
    
    def show_input_dialog(self, title, prompt, initial_value=""):
        """Mostra uma janela de diálogo para entrada de dados"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.configure(bg="#100720")
        dialog.transient(self.root) # Make dialog transient to the root window
        dialog.grab_set() # Grab all events until dialog is destroyed
        
        tk.Label(dialog, text=prompt, bg="#100720", fg="white", font=("Arial", 11)).pack(pady=15)
        
        entry_var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(dialog, textvariable=entry_var, width=35)
        entry.pack(pady=10, ipady=3)
        entry.focus_set()
        
        result = []
        
        def on_ok():
            result.append(entry_var.get())
            dialog.destroy()
        
        def on_cancel():
            result.append(None)
            dialog.destroy()
        
        button_frame = tk.Frame(dialog, bg="#100720")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="OK", command=on_ok, style='Menu.TButton').pack(side=tk.LEFT, padx=15)
        ttk.Button(button_frame, text="Cancelar", command=on_cancel, style='Danger.TButton').pack(side=tk.RIGHT, padx=15)
        
        self.root.wait_window(dialog) # Wait for the dialog to close
        return result[0] if result else None
    
    def update_user_field(self, field, new_value):
        """Atualiza um campo do usuário no banco de dados"""
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute(f'UPDATE usuarios SET {field} = ? WHERE id = ?', 
                           (new_value.strip(), self.user_data['id']))
            conn.commit()
            
            # Atualizar dados do usuário na memória
            self.user_data[field] = new_value.strip()
            self.entry_vars[field].set(new_value.strip())
            
            messagebox.showinfo("Sucesso", f"{field.capitalize()} atualizado com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao atualizar {field}: {str(e)}")
        finally:
            conn.close()
    
    def change_password(self):
        """Processo de alteração de senha com 2FA"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Alterar Senha")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.configure(bg="#100720")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Critérios da Senha:\n• Exatamente 6 caracteres\n• Sem espaços", 
                 bg="#100720", fg="white", font=("Arial", 10, "italic")).pack(pady=10)

        # Frame para nova senha
        new_pass_frame = tk.Frame(dialog, bg="#100720")
        new_pass_frame.pack(pady=10)
        
        tk.Label(new_pass_frame, text="Nova Senha:", bg="#100720", fg="white", font=("Arial", 11)).pack(side=tk.LEFT)
        new_pass_var = tk.StringVar()
        new_pass_entry = ttk.Entry(new_pass_frame, textvariable=new_pass_var, show="*", width=30)
        new_pass_entry.pack(side=tk.LEFT, padx=5, ipady=3)
        
        show_btn = ttk.Button(new_pass_frame, text="👁️", width=4,
                              command=lambda: self.toggle_password_visibility(new_pass_entry))
        show_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame para confirmar senha
        confirm_frame = tk.Frame(dialog, bg="#100720")
        confirm_frame.pack(pady=10)
        
        tk.Label(confirm_frame, text="Confirmar Senha:", bg="#100720", fg="white", font=("Arial", 11)).pack(side=tk.LEFT)
        confirm_pass_var = tk.StringVar()
        confirm_pass_entry = ttk.Entry(confirm_frame, textvariable=confirm_pass_var, show="*", width=30)
        confirm_pass_entry.pack(side=tk.LEFT, padx=5, ipady=3)
        
        show_btn = ttk.Button(confirm_frame, text="👁️", width=4,
                              command=lambda: self.toggle_password_visibility(confirm_pass_entry))
        show_btn.pack(side=tk.RIGHT, padx=5)
        
       
        
        def validate_and_proceed():
            nova_senha = new_pass_var.get().strip()
            confirmar_senha = confirm_pass_var.get().strip()
            
            if len(nova_senha) != 6 or " " in nova_senha: # Removido .replace(" ", "") para validar espaços
                messagebox.showerror("Erro", "Senha inválida. Deve ter exatamente 6 caracteres sem espaços.")
                return
            
            if nova_senha != confirmar_senha:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return
            
            # Gerar código 2FA
            codigo = str(random.randint(100000, 999999))
            expiration_time = datetime.now() + timedelta(minutes=5)
            
            # Enviar código por email
            try:
                msg = MIMEText(f"Seu código de verificação para alteração de senha é: {codigo}\n\nEste código é válido por 5 minutos.")
                msg['Subject'] = 'Código de Verificação - Alteração de Senha'
                msg['From'] = self.EMAIL_SENDER
                msg['To'] = self.user_data['email']
                
                with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                    server.starttls()
                    server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                    server.sendmail(self.EMAIL_SENDER, self.user_data['email'], msg.as_string())
                
                # Mostrar campo para inserir código
                for widget in dialog.winfo_children():
                    widget.destroy()
                
                dialog.geometry("400x200")
                
                tk.Label(dialog, text="Digite o código de 6 dígitos enviado para seu email:", 
                         bg="#100720", fg="white", font=("Arial", 11)).pack(pady=15)
                
                tk.Label(dialog, text="(Código válido por 5 minutos)", 
                         bg="#100720", fg="white", font=("Arial", 9, "italic")).pack()
                
                code_var = tk.StringVar()
                ttk.Entry(dialog, textvariable=code_var, width=12, 
                          font=("Arial", 16), justify="center").pack(pady=10, ipady=3)
                
                def verify_code():
                    if datetime.now() > expiration_time:
                        messagebox.showerror("Erro", "Código expirado. Por favor, inicie o processo novamente.")
                        dialog.destroy()
                        return
    
                    if code_var.get() == codigo:
        # Atualizar senha no banco de dados
                        conn = sqlite3.connect('usuarios.db')
                        cursor = conn.cursor()
                        cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', 
                       (nova_senha, self.user_data['id']))
                        
                        conn.commit()
                        conn.close()
        
                        messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                        dialog.destroy()
                        self.entry_vars["senha"].set("******")
                    else:
                        messagebox.showerror("Erro", "Código incorreto. Tente novamente.")

# Criar estilo para o botão Verificar
                style = ttk.Style()
                style.configure('Verify.TButton', 
                                font=('Arial', 12),
                                foreground='black',
                                background='white',
                                padding=8)
                style.map('Verify.TButton',
                        background=[('active', '#e0e0e0')],
                        foreground=[('active', 'black')])

# Criar o botão Verificar com o novo estilo
                verify_btn = ttk.Button(dialog, 
                        text="Verificar", 
                        command=verify_code, 
                        style='Verify.TButton')
                verify_btn.pack(pady=15)
                

                
                
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao enviar código: {str(e)}\nVerifique suas credenciais e conexão de internet.")
                dialog.destroy()
        
        ttk.Button(dialog, text="Continuar", command=validate_and_proceed, style='Accent.TButton').pack(pady=20)
        self.root.wait_window(dialog)
    
    def confirmar_exclusao_conta(self):
        """Inicia o processo de exclusão de conta com 2FA"""
        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita."):
            return
        
        # Gerar código 2FA
        codigo = str(random.randint(100000, 999999))
        expiration_time = datetime.now() + timedelta(minutes=5)
        
        # Enviar código por email
        try:
            msg = MIMEText(f"Seu código de verificação para exclusão de conta é: {codigo}\n\nEste código é válido por 5 minutos.")
            msg['Subject'] = 'Código de Verificação - Exclusão de Conta'
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = self.user_data['email']
            
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
                server.sendmail(self.EMAIL_SENDER, self.user_data['email'], msg.as_string())
            
            # Mostrar diálogo para inserir código
            dialog = tk.Toplevel(self.root)
            dialog.title("Verificação de Exclusão")
            dialog.geometry("450x220")
            dialog.resizable(False, False)
            dialog.configure(bg="#100720")
            dialog.transient(self.root)
            dialog.grab_set()
            
            tk.Label(dialog, text="Digite o código de 6 dígitos enviado para seu email:", 
                     bg="#100720", fg="white", font=("Arial", 11)).pack(pady=15)
            
            tk.Label(dialog, text="(Código válido por 5 minutos)", 
                     bg="#100720", fg="white", font=("Arial", 9, "italic")).pack()
            
            code_var = tk.StringVar()
            ttk.Entry(dialog, textvariable=code_var, width=12, 
                      font=("Arial", 16), justify="center").pack(pady=10, ipady=3)
            
            def verify_and_delete():
                if datetime.now() > expiration_time:
                    messagebox.showerror("Erro", "Código expirado. Por favor, inicie o processo novamente.")
                    dialog.destroy()
                    return
                
                if code_var.get() == codigo:
                    dialog.destroy()
                    self.excluir_conta()
                else:
                    messagebox.showerror("Erro", "Código incorreto. Tente novamente.")
            
            ttk.Button(dialog, text="Verificar e Excluir", command=verify_and_delete, style='Danger.TButton').pack(pady=15)
            self.root.wait_window(dialog)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar código: {str(e)}\nVerifique suas credenciais e conexão de internet.")
    
    def excluir_conta(self):
        """Exclui a conta do usuário do banco de dados"""
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (self.user_data['id'],))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
            
            # Fechar menu e voltar para tela de cadastro
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Reiniciar o sistema de cadastro
            self.sistema_cadastro.setup_interface()
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao excluir conta: {str(e)}")
        finally:
            conn.close()
    
    def show_sobre(self):
        """Mostra a seção Sobre"""
        if self.current_section == "sobre":
            return
            
        self.clear_content_frame()
        self.current_section = "sobre"
        
        tk.Label(self.content_frame, text="ℹ️ Sobre", font=("Times New Roman", 22, "bold"), 
                 bg="#100720", fg="white").pack(pady=20)
        
        about_frame = tk.Frame(self.content_frame, bg="#100720", highlightbackground="#3D087B", 
                               highlightthickness=3, bd=0, relief="sunken")
        about_frame.pack(pady=25, padx=80, fill=tk.X)
        
        about_text = """
        Na Pele e na Consciência - Um Simulador de Dilemas Éticos
        
        Este é um jogo que coloca você em situações desafiadoras
        para refletir sobre questões sociais e éticas.
        
        Desenvolvido para promover empatia e compreensão
        sobre diferentes realidades sociais.
        
        Versão: 1.0.0
        Desenvolvedor: Ana Clara Souza
        """
        
        tk.Label(about_frame, text=about_text, font=("Times New Roman", 14), 
                 bg="#100720", fg="white", justify=tk.LEFT).pack(pady=20, padx=20)

        # Adicionar uma linha divisória visual
        ttk.Separator(self.content_frame, orient='horizontal').pack(fill='x', padx=50, pady=10)
        tk.Label(self.content_frame, text="Agradecemos por jogar!", 
                 font=("Times New Roman", 12, "italic"), bg="#100720", fg="#C0C0C0").pack(pady=10)


    def show_ajuda(self):
        """Mostra a seção Ajuda"""
        if self.current_section == "ajuda":
            return
            
        self.clear_content_frame()
        self.current_section = "ajuda"
        
        tk.Label(self.content_frame, text="❓ Ajuda", font=("Times New Roman", 22, "bold"), 
                 bg="#100720", fg="white").pack(pady=20)
        
        help_frame = tk.Frame(self.content_frame, bg="#100720", highlightbackground="#3D087B", 
                              highlightthickness=3, bd=0, relief="groove")
        # Ajustando o padx para aumentar a largura da moldura
        help_frame.pack(pady=25, padx=50, fill=tk.X) # Reduzido padx de 80 para 50 para ampliar a moldura
        
        help_text = """
        Como usar o sistema:
        
        1. Mundos de Consciência: Escolha uma categoria para jogar e mergulhe em dilemas éticos.
        2. Perfil Personalizado: Acompanhe seu progresso, veja suas escolhas e o impacto delas.
        3. Configurações de Perfil: Edite seus dados pessoais, como nome, apelido, email ou senha, e gerencie sua conta.
        
        Dicas de Jogo:
        • Cada escolha importa. Pense bem antes de decidir!
        • Explore todas as opções para entender as nuances dos dilemas.
        
        Para dúvidas ou problemas, entre em contato com:
        napeleenaconsciencia@gmail.com
        """
        
        tk.Label(help_frame, text=help_text, font=("Times New Roman", 14), 
                 bg="#100720", fg="white", justify=tk.LEFT, wraplength=550).pack(pady=20, padx=20) # Aumentado wraplength
        
        # Adicionar um botão de "FAQ" ou "Perguntas Frequentes"
        style = ttk.Style()
        style.configure('Help.TButton', font=('Arial', 11, 'bold'), padding=8, 
                        foreground='black', background='white', borderwidth=2, relief="ridge")
        style.map('Help.TButton', background=[('active', '#e0e0e0')], foreground=[('active', 'black')])

        ttk.Button(self.content_frame, text="Ver Perguntas Frequentes (FAQ)", 
                   command=lambda: messagebox.showinfo("FAQ", "Funcionalidade em desenvolvimento!"),
                   style='Help.TButton').pack(pady=20)
    

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Esta função é chamada pelo sistema de cadastro após a inicialização
        self.setup_home_screen()
