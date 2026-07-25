"""
Dashboard da interface - A.R.G.U.S.
"""

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkTextbox, CTkEntry, CTkProgressBar, CTkImage, CTkOptionMenu
from PIL import Image
import cv2
import threading
import time
from config import COLORS, UPDATE_INTERVAL
from monitor import monitor
from network import network
from ai import ai
from database import db
from graphs import graph_manager
from webcam import webcam
from auth import authenticate_user, register_user
from notifications import send_notification
from i18n import get_current_language, get_text, set_language
from automation import run_automation_tasks
from reports import export_summary_report
from plugins import run_plugins
from voice import voice_assistant
from api_server import app as api_app
from threading import Thread
import webbrowser
from api_server import get_api_token
from themes import get_theme_preference, set_theme_preference
from integrations import load_config, save_config, trigger_integrations, sync_to_cloud
from two_factor import get_secret, generate_qr_code, verify_totp_code, set_secret


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("A.R.G.U.S. v3.0 - Sistema de Monitoramento em Tempo Real")
        self.root.geometry("1400x900")
        self.root.configure(fg_color=COLORS['bg_primary'])
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', lambda event: self.root.attributes('-fullscreen', False))
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.monitoring = True
        self.update_thread = None
        self.webcam_thread = None
        self.webcam_image = None
        self.api_thread = None
        self.api_running = False
        self.current_language = get_current_language()
        self.logged_in = False
        self.current_theme = get_theme_preference()
        
        self.setup_ui()
        self.start_monitoring()
        self.show_login_window()

    def toggle_fullscreen(self, event=None):
        """Alterna tela cheia; F11 ativa e Escape sai."""
        self.root.attributes("-fullscreen", not bool(self.root.attributes("-fullscreen")))
    def setup_ui(self):
        """Configura a interface do usuÃ¡rio"""
        # Container principal com scroll
        main_container = CTkFrame(self.root, fg_color=COLORS['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header(main_container)
        
        # ConteÃºdo principal com duas colunas
        content = CTkFrame(main_container, fg_color=COLORS['bg_primary'])
        content.pack(fill="both", expand=True, pady=10)
        
        # Coluna esquerda - Monitoramento
        left_col = CTkFrame(content, fg_color=COLORS['bg_primary'])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Coluna direita - IA e Eventos
        right_col = CTkFrame(content, fg_color=COLORS['bg_primary'])
        right_col.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.setup_monitoring_panel(left_col)
        self.setup_ai_panel(right_col)
        self.setup_webcam_panel(right_col)
        
        # Footer
        self.setup_footer(main_container)

    def setup_header(self, parent):
        """Configura o header da aplicaÃ§Ã£o"""
        header = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        header.pack(fill="x", pady=(0, 10))
        
        title = CTkLabel(
            header,
            text=get_text('title', self.current_language),
            font=("Arial", 28, "bold"),
            text_color=COLORS['accent_green']
        )
        title.pack(pady=15)
        
        subtitle = CTkLabel(
            header,
            text="Sistema AvanÃ§ado de Reconhecimento, Gerenciamento e VigilÃ¢ncia",
            font=("Arial", 12),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 15))

        self.header_label = title

    def setup_monitoring_panel(self, parent):
        """Configura o painel de monitoramento"""
        # Frame do monitoramento
        monitor_frame = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        monitor_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        title = CTkLabel(
            monitor_frame,
            text="ðŸ“Š MONITORAMENTO DO SISTEMA",
            font=("Arial", 14, "bold"),
            text_color=COLORS['accent_green']
        )
        title.pack(pady=10)
        
        # Ãrea de scroll para os monitores
        scroll_frame = CTkFrame(monitor_frame, fg_color=COLORS['bg_secondary'])
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CPU
        self.create_stat_widget(scroll_frame, "CPU", "cpu_label", "cpu_progress")
        
        # RAM
        self.create_stat_widget(scroll_frame, "RAM", "ram_label", "ram_progress")
        
        # GPU
        self.create_stat_widget(scroll_frame, "GPU", "gpu_label", "gpu_progress")
        
        # Disco
        self.create_stat_widget(scroll_frame, "DISCO", "disk_label", "disk_progress")
        
        # Temperatura
        temp_frame = CTkFrame(scroll_frame, fg_color=COLORS['bg_primary'], corner_radius=8)
        temp_frame.pack(fill="x", pady=5)
        
        temp_label = CTkLabel(
            temp_frame,
            text="Temperatura",
            font=("Arial", 11, "bold"),
            text_color=COLORS['text_primary']
        )
        temp_label.pack(side="left", padx=10, pady=8)
        
        self.temp_label = CTkLabel(
            temp_frame,
            text="--Â°C",
            font=("Arial", 11, "bold"),
            text_color=COLORS['accent_yellow']
        )
        self.temp_label.pack(side="right", padx=10, pady=8)
        
        # Processos e Status
        info_frame = CTkFrame(scroll_frame, fg_color=COLORS['bg_primary'], corner_radius=8)
        info_frame.pack(fill="x", pady=5)
        
        self.processes_label = CTkLabel(
            info_frame,
            text="Processos: --",
            font=("Arial", 10),
            text_color=COLORS['text_secondary']
        )
        self.processes_label.pack(side="left", padx=10, pady=8)
        
        self.status_label = CTkLabel(
            info_frame,
            text="Status: --",
            font=("Arial", 10, "bold"),
            text_color=COLORS['accent_green']
        )
        self.status_label.pack(side="right", padx=10, pady=8)

    def create_stat_widget(self, parent, name, label_id, progress_id):
        """Cria um widget de estatÃ­stica"""
        stat_frame = CTkFrame(parent, fg_color=COLORS['bg_primary'], corner_radius=8)
        stat_frame.pack(fill="x", pady=5)
        
        # Nome
        name_label = CTkLabel(
            stat_frame,
            text=name,
            font=("Arial", 11, "bold"),
            text_color=COLORS['text_primary']
        )
        name_label.pack(side="left", padx=10, pady=8)
        
        # Percentual
        setattr(self, label_id, CTkLabel(
            stat_frame,
            text="0%",
            font=("Arial", 11, "bold"),
            text_color=COLORS['accent_green']
        ))
        getattr(self, label_id).pack(side="right", padx=10, pady=8)
        
        # Progress Bar
        setattr(self, progress_id, CTkProgressBar(
            stat_frame,
            fg_color=COLORS['border'],
            progress_color=COLORS['accent_green'],
            height=5
        ))
        getattr(self, progress_id).set(0)
        getattr(self, progress_id).pack(side="left", fill="x", expand=True, padx=10, pady=8)

    def setup_ai_panel(self, parent):
        """Configura o painel de IA"""
        ai_frame = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        ai_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        title = CTkLabel(
            ai_frame,
            text="ðŸ¤– ASSISTENTE A.R.G.U.S.",
            font=("Arial", 14, "bold"),
            text_color=COLORS['accent_blue']
        )
        title.pack(pady=10)
        
        # Caixa de conversa
        self.chat_box = CTkTextbox(
            ai_frame,
            width=400,
            height=300,
            fg_color=COLORS['bg_primary'],
            text_color=COLORS['text_primary'],
            border_color=COLORS['border'],
            border_width=2,
            corner_radius=8
        )
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat_box.configure(state="disabled")
        
        # Entrada de texto
        input_frame = CTkFrame(ai_frame, fg_color=COLORS['bg_secondary'])
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_field = CTkEntry(
            input_frame,
            placeholder_text="Digite algo para conversar...",
            fg_color=COLORS['bg_primary'],
            border_color=COLORS['border'],
            text_color=COLORS['text_primary'],
            placeholder_text_color=COLORS['text_secondary']
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)
        
        send_btn = CTkButton(
            input_frame,
            text="Enviar",
            fg_color=COLORS['accent_blue'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            width=80,
            command=self.send_message
        )
        send_btn.pack(side="right")
        
        # Exibir saudaÃ§Ã£o inicial
        greeting = ai.get_greeting()
        self.add_to_chat(f"A.R.G.U.S.: {greeting}")

    def setup_webcam_panel(self, parent):
        """Configura o painel de webcam"""
        webcam_frame = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        webcam_frame.pack(fill="both", expand=True, pady=(0, 10))

        title = CTkLabel(
            webcam_frame,
            text="ðŸŽ¥ WEBCAM",
            font=("Arial", 14, "bold"),
            text_color=COLORS['accent_blue']
        )
        title.pack(pady=10)

        preview_frame = CTkFrame(webcam_frame, fg_color=COLORS['bg_primary'], corner_radius=8)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.webcam_preview_label = CTkLabel(
            preview_frame,
            text="Webcam offline",
            font=("Arial", 11),
            text_color=COLORS['text_secondary'],
            width=640,
            height=360,
            anchor="center"
        )
        self.webcam_preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        controls_frame = CTkFrame(webcam_frame, fg_color=COLORS['bg_primary'], corner_radius=8)
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        fullscreen_webcam_btn = CTkButton(
            controls_frame,
            text="Abrir em tela cheia",
            fg_color=COLORS['accent_blue'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.open_webcam_page
        )
        fullscreen_webcam_btn.pack(side="left", expand=True, padx=5, pady=5)
        self.start_webcam_btn = CTkButton(
            controls_frame,
            text="Iniciar Webcam",
            fg_color=COLORS['accent_green'],
            hover_color=COLORS['accent_blue'],
            text_color=COLORS['bg_primary'],
            command=self.start_webcam
        )
        self.start_webcam_btn.pack(side="left", expand=True, padx=5, pady=5)

        self.stop_webcam_btn = CTkButton(
            controls_frame,
            text="Parar Webcam",
            fg_color=COLORS['accent_red'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.stop_webcam,
            state="disabled"
        )
        self.stop_webcam_btn.pack(side="left", expand=True, padx=5, pady=5)

        self.snapshot_btn = CTkButton(
            controls_frame,
            text="Salvar Foto",
            fg_color=COLORS['accent_yellow'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.save_webcam_snapshot,
            state="disabled"
        )
        self.snapshot_btn.pack(side="left", expand=True, padx=5, pady=5)

        status_frame = CTkFrame(webcam_frame, fg_color=COLORS['bg_primary'], corner_radius=8)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.webcam_status_label = CTkLabel(
            status_frame,
            text="Status: Offline",
            font=("Arial", 11),
            text_color=COLORS['text_secondary']
        )
        self.webcam_status_label.pack(side="left", padx=10, pady=8)

    def open_webcam_page(self):
        """Abre a visualização grande no navegador local autenticado."""
        if not self.api_running:
            self.toggle_api_server()
        token = get_api_token()
        self.root.after(700, lambda: webbrowser.open("http://127.0.0.1:5000/webcam?token=" + token))
    def start_webcam(self):
        """Inicia a webcam e mostra o preview"""
        if webcam.is_recording or self.webcam_thread is not None:
            return

        self.add_to_chat("A.R.G.U.S.: Solicitando permissÃ£o da webcam...")
        self.webcam_status_label.configure(text="Status: Inicializando webcam...")
        self._set_webcam_buttons(running=True)

        def run_webcam_start():
            started = webcam.start_recording()
            self.root.after(0, self._on_webcam_started, started)

        self.webcam_thread = threading.Thread(target=run_webcam_start, daemon=True)
        self.webcam_thread.start()

    def _on_webcam_started(self, started: bool):
        if not started:
            self.webcam_status_label.configure(text="Status: Erro ao iniciar")
            self.add_to_chat("A.R.G.U.S.: Erro ao acessar a webcam. Verifique se ela estÃ¡ conectada e nÃ£o estÃ¡ em uso.")
            self._set_webcam_buttons(running=False)
            self.webcam_thread = None
            return

        self.webcam_status_label.configure(text="Status: Webcam ativa")
        self.webcam_preview_label.configure(text="Aguardando frames...", image=None)
        self.snapshot_btn.configure(state="normal")
        self.root.after(100, self.update_webcam_preview)
        self.add_to_chat("A.R.G.U.S.: Webcam ativada com sucesso.")
        self.webcam_thread = None

    def update_webcam_preview(self):
        """Atualiza o preview da webcam na UI"""
        if not webcam.is_recording:
            return

        try:
            frame = webcam.frame
            if frame is None:
                self.webcam_preview_label.configure(text="Aguardando frames...", image=None)
            else:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb).resize((640, 360))
                self.webcam_image = CTkImage(light_image=image, size=(640, 360))
                self.webcam_preview_label.configure(image=self.webcam_image, text="")
        except Exception as e:
            print(f"Erro ao atualizar preview da webcam: {e}")

        self.root.after(100, self.update_webcam_preview)

    def stop_webcam(self):
        """Para a webcam em execuÃ§Ã£o"""
        if not webcam.is_recording:
            return

        webcam.stop_recording()
        self.webcam_status_label.configure(text="Status: Offline")
        self.webcam_preview_label.configure(image=None, text="Webcam parada")
        self._set_webcam_buttons(running=False)
        self.webcam_image = None
        self.add_to_chat("A.R.G.U.S.: Webcam desligada.")
        self.webcam_thread = None

    def _set_webcam_buttons(self, running: bool):
        self.start_webcam_btn.configure(state="disabled" if running else "normal")
        self.stop_webcam_btn.configure(state="normal" if running else "disabled")
        self.snapshot_btn.configure(state="normal" if running else "disabled")

    def save_webcam_snapshot(self):
        """Salva um snapshot da webcam"""
        if webcam.frame is None:
            self.add_to_chat("A.R.G.U.S.: Nenhum frame disponÃ­vel para salvar.")
            return

        if webcam.save_snapshot('snapshot'):
            self.add_to_chat("A.R.G.U.S.: Snapshot salvo em assets/")
        else:
            self.add_to_chat("A.R.G.U.S.: Falha ao salvar snapshot.")

    def setup_footer(self, parent):
        """Configura o footer"""
        footer = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        footer.pack(fill="x")
        
        # InformaÃ§Ãµes de rede
        info_text = CTkLabel(
            footer,
            text="IP: -- | Velocidade: -- Mbps | Status: Conectando...",
            font=("Arial", 10),
            text_color=COLORS['text_secondary']
        )
        info_text.pack(pady=10)
        
        self.footer_label = info_text
        
        button_frame = CTkFrame(footer, fg_color=COLORS['bg_secondary'])
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        speed_test_btn = CTkButton(
            button_frame,
            text="Teste de Velocidade",
            fg_color=COLORS['accent_yellow'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.start_speed_test
        )
        speed_test_btn.pack(side="left", padx=5)
        
        clear_btn = CTkButton(
            button_frame,
            text="Limpar Chat",
            fg_color=COLORS['accent_red'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.clear_chat
        )
        clear_btn.pack(side="left", padx=5)

        self.lang_option_menu = CTkOptionMenu(
            button_frame,
            values=["pt-BR", "en-US"],
            command=self.change_language,
            width=120,
        )
        self.lang_option_menu.set(self.current_language)
        self.lang_option_menu.pack(side="left", padx=5)

        api_btn = CTkButton(
            button_frame,
            text=get_text('api_start', self.current_language),
            fg_color=COLORS['accent_blue'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.toggle_api_server,
        )
        api_btn.pack(side="left", padx=5)

        report_btn = CTkButton(
            button_frame,
            text=get_text('export_pdf', self.current_language),
            fg_color=COLORS['accent_green'],
            hover_color=COLORS['accent_blue'],
            text_color=COLORS['bg_primary'],
            command=self.export_report,
        )
        report_btn.pack(side="left", padx=5)

        automation_btn = CTkButton(
            button_frame,
            text=get_text('cleanup', self.current_language),
            fg_color=COLORS['accent_yellow'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.run_automation,
        )
        automation_btn.pack(side="left", padx=5)

        notification_btn = CTkButton(
            button_frame,
            text=get_text('notify_test', self.current_language),
            fg_color=COLORS['accent_red'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.send_test_notification,
        )
        notification_btn.pack(side="left", padx=5)

        theme_btn = CTkButton(
            button_frame,
            text="Tema",
            fg_color=COLORS['accent_yellow'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.toggle_theme,
        )
        theme_btn.pack(side="left", padx=5)

        integration_btn = CTkButton(
            button_frame,
            text="IntegraÃ§Ãµes",
            fg_color=COLORS['accent_blue'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.show_integration_window,
        )
        integration_btn.pack(side="left", padx=5)

        cloud_btn = CTkButton(
            button_frame,
            text="Nuvem",
            fg_color=COLORS['accent_green'],
            hover_color=COLORS['accent_blue'],
            text_color=COLORS['bg_primary'],
            command=self.sync_to_cloud,
        )
        cloud_btn.pack(side="left", padx=5)

        twofa_btn = CTkButton(
            button_frame,
            text="2FA",
            fg_color=COLORS['accent_red'],
            hover_color=COLORS['accent_green'],
            text_color=COLORS['bg_primary'],
            command=self.show_two_factor_window,
        )
        twofa_btn.pack(side="left", padx=5)

        self.api_btn = api_btn
        self.theme_btn = theme_btn

    def send_message(self, event=None):
        """Envia uma mensagem para a IA"""
        message = self.input_field.get().strip()
        
        if not message:
            return

        self.add_to_chat(f"VocÃª: {message}")
        self.input_field.delete(0, "end")

        message_lower = message.lower()
        if any(cmd in message_lower for cmd in [
            "ligue a webcam",
            "ligar webcam",
            "ligue webcam",
            "ativar webcam",
            "ativa webcam",
            "abrir webcam",
            "abrir cÃ¢mera",
            "ligar a cÃ¢mera",
            "ligue a cÃ¢mera"
        ]):
            self.add_to_chat("A.R.G.U.S.: Recebido. Iniciando a webcam...")
            self.start_webcam()
            ai.add_to_history(message, "Comando de webcam recebido.")
            return

        if any(cmd in message_lower for cmd in [
            "desligue a webcam",
            "desligar webcam",
            "parar webcam",
            "fechar webcam",
            "desligar a cÃ¢mera",
            "parar cÃ¢mera"
        ]):
            self.add_to_chat("A.R.G.U.S.: Entendido. Desligando a webcam...")
            self.stop_webcam()
            ai.add_to_history(message, "Comando de webcam recebido.")
            return

        if any(cmd in message_lower for cmd in ["exportar pdf", "export pdf", "pdf"]):
            self.export_report()
            self.add_to_chat("A.R.G.U.S.: RelatÃ³rio exportado.")
            return

        if any(cmd in message_lower for cmd in ["plugin", "plugins"]):
            results = run_plugins()
            self.add_to_chat("A.R.G.U.S.: " + " | ".join(results or ["Nenhum plugin encontrado"]))
            return

        if any(cmd in message_lower for cmd in ["fala", "falar", "voice", "voz"]):
            voice_assistant.speak("Assistente A R G U S ativo")
            self.add_to_chat("A.R.G.U.S.: Comando de voz processado.")
            return

        response = ai.get_response(message)
        self.add_to_chat(f"A.R.G.U.S.: {response}")
        ai.add_to_history(message, response)

    def add_to_chat(self, message):
        """Adiciona uma mensagem ao chat"""
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", message + "\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def clear_chat(self):
        """Limpa o chat"""
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.chat_box.configure(state="disabled")

    def start_speed_test(self):
        """Inicia o teste de velocidade"""
        self.add_to_chat("A.R.G.U.S.: Iniciando teste de velocidade... Isso pode levar alguns minutos.")
        
        def run_test():
            result = network.test_speed()
            if result:
                message = f"Teste concluÃ­do!\nDownload: {result['download']:.2f} Mbps\nUpload: {result['upload']:.2f} Mbps"
                self.add_to_chat(f"A.R.G.U.S.: {message}")
            else:
                self.add_to_chat("A.R.G.U.S.: Erro ao executar teste de velocidade.")
        
        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def start_monitoring(self):
        """Inicia o thread de monitoramento"""
        self.update_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.update_thread.start()

    def show_login_window(self):
        """Mostra uma janela simples de login antes de liberar o dashboard."""
        if self.logged_in:
            return

        login_window = ctk.CTkToplevel(self.root)
        login_window.title(get_text('login_title', self.current_language))
        login_window.geometry("360x260")
        login_window.transient(self.root)
        login_window.grab_set()

        ctk.CTkLabel(login_window, text=get_text('login_title', self.current_language), font=("Arial", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(login_window, text="Crie o primeiro usuário com uma senha de pelo menos 12 caracteres.", font=("Arial", 10)).pack(pady=(0, 10))

        self.login_username = ctk.CTkEntry(login_window, placeholder_text=get_text('username', self.current_language))
        self.login_username.pack(padx=20, pady=5, fill="x")
        self.login_password = ctk.CTkEntry(login_window, placeholder_text=get_text('password', self.current_language), show="*")
        self.login_password.pack(padx=20, pady=5, fill="x")

        def handle_login():
            user = self.login_username.get().strip()
            password = self.login_password.get().strip()
            if authenticate_user(user, password):
                self.logged_in = True
                self.add_to_chat("A.R.G.U.S.: Login realizado com sucesso.")
                login_window.destroy()
            else:
                self.add_to_chat(f"A.R.G.U.S.: {get_text('login_failed', self.current_language)}")

        ctk.CTkButton(login_window, text=get_text('login', self.current_language), command=handle_login).pack(pady=10)
        ctk.CTkButton(login_window, text=get_text('register', self.current_language), command=lambda: self.register_user_dialog(login_window)).pack()

    def register_user_dialog(self, parent):
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Registrar")
        dialog.geometry("320x220")
        dialog.transient(parent)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Novo usuÃ¡rio", font=("Arial", 14, "bold")).pack(pady=10)
        username = ctk.CTkEntry(dialog, placeholder_text="UsuÃ¡rio")
        username.pack(padx=20, pady=5, fill="x")
        password = ctk.CTkEntry(dialog, placeholder_text="Senha", show="*")
        password.pack(padx=20, pady=5, fill="x")

        def handle_register():
            if register_user(username.get().strip(), password.get().strip()):
                self.add_to_chat("A.R.G.U.S.: UsuÃ¡rio registrado com sucesso.")
                dialog.destroy()
            else:
                self.add_to_chat("A.R.G.U.S.: Falha ao registrar usuÃ¡rio.")

        ctk.CTkButton(dialog, text="Registrar", command=handle_register).pack(pady=10)

    def change_language(self, choice):
        self.current_language = choice
        set_language(choice)
        self.header_label.configure(text=get_text('title', self.current_language))
        self.api_btn.configure(text=get_text('api_start' if not self.api_running else 'api_stop', self.current_language))
        self.lang_option_menu.set(choice)
        self.add_to_chat("A.R.G.U.S.: " + get_text('language_saved', self.current_language))

    def send_test_notification(self):
        send_notification("A.R.G.U.S.", "Teste de notificaÃ§Ã£o enviado")
        self.add_to_chat("A.R.G.U.S.: NotificaÃ§Ã£o enviada.")

    def export_report(self):
        path = export_summary_report(
            {
                "cpu": monitor.cpu_usage,
                "ram": monitor.ram_usage,
                "disk": monitor.disk_usage,
                "temperature": monitor.temperature,
                "processes": monitor.processes_count,
            },
            ["Status normal"],
        )
        self.add_to_chat(f"A.R.G.U.S.: {get_text('report_saved', self.current_language)} -> {path}")

    def run_automation(self):
        result = run_automation_tasks()
        self.add_to_chat(f"A.R.G.U.S.: {get_text('cleanup_done', self.current_language)} / {get_text('backup_done', self.current_language)}")
        if result.get('backup', {}).get('path'):
            self.add_to_chat(f"A.R.G.U.S.: Backup -> {result['backup']['path']}")

    def toggle_api_server(self):
        if self.api_running:
            self.api_running = False
            self.api_btn.configure(text=get_text('api_start', self.current_language))
            self.add_to_chat("A.R.G.U.S.: API parada.")
            return

        self.api_running = True
        self.api_btn.configure(text=get_text('api_stop', self.current_language))
        self.add_to_chat("A.R.G.U.S.: API iniciada em http://127.0.0.1:5000")

        def run_api():
            api_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

        self.api_thread = Thread(target=run_api, daemon=True)
        self.api_thread.start()

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        set_theme_preference(self.current_theme)
        ctk.set_appearance_mode(self.current_theme)
        self.theme_btn.configure(text='Tema: ' + ('Claro' if self.current_theme == 'light' else 'Escuro'))
        self.add_to_chat(f"A.R.G.U.S.: Tema alterado para {self.current_theme}")

    def show_integration_window(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Configurar IntegraÃ§Ãµes")
        dialog.geometry("420x360")
        dialog.transient(self.root)
        dialog.grab_set()

        config = load_config()
        telegram_token = ctk.CTkEntry(dialog, placeholder_text="Telegram Token")
        telegram_token.pack(padx=20, pady=5, fill="x")
        telegram_chat = ctk.CTkEntry(dialog, placeholder_text="Telegram Chat ID")
        telegram_chat.pack(padx=20, pady=5, fill="x")
        discord_webhook = ctk.CTkEntry(dialog, placeholder_text="Discord Webhook")
        discord_webhook.pack(padx=20, pady=5, fill="x")
        cloud_folder = ctk.CTkEntry(dialog, placeholder_text="Pasta de backup")
        cloud_folder.pack(padx=20, pady=5, fill="x")

        telegram_token.insert(0, config.get('telegram', {}).get('token', ''))
        telegram_chat.insert(0, config.get('telegram', {}).get('chat_id', ''))
        discord_webhook.insert(0, config.get('discord', {}).get('webhook', ''))
        cloud_folder.insert(0, config.get('cloud', {}).get('folder', 'database/cloud_backup'))

        def save_integration():
            config['telegram'] = {'enabled': True, 'token': telegram_token.get().strip(), 'chat_id': telegram_chat.get().strip()}
            config['discord'] = {'enabled': True, 'webhook': discord_webhook.get().strip()}
            config['cloud'] = {'enabled': True, 'folder': cloud_folder.get().strip()}
            save_config(config)
            self.add_to_chat("A.R.G.U.S.: IntegraÃ§Ãµes configuradas.")
            dialog.destroy()

        ctk.CTkButton(dialog, text="Salvar", command=save_integration).pack(pady=10)

    def sync_to_cloud(self):
        result = sync_to_cloud()
        self.add_to_chat(f"A.R.G.U.S.: SincronizaÃ§Ã£o em nuvem -> {result}")

    def show_two_factor_window(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Configurar 2FA")
        dialog.geometry("400x280")
        dialog.transient(self.root)
        dialog.grab_set()

        secret = get_secret() or set_secret("")
        qr_uri = generate_qr_code(secret or "")
        ctk.CTkLabel(dialog, text="QR Code / URI", font=("Arial", 13, "bold")).pack(pady=8)
        ctk.CTkLabel(dialog, text=qr_uri, wraplength=340, justify="center").pack(padx=10)

        code_entry = ctk.CTkEntry(dialog, placeholder_text="CÃ³digo temporÃ¡rio")
        code_entry.pack(padx=20, pady=10, fill="x")

        def save_secret():
            new_secret = code_entry.get().strip() or secret
            set_secret(new_secret)
            self.add_to_chat("A.R.G.U.S.: Segredo 2FA atualizado.")
            dialog.destroy()

        def verify_code():
            code = code_entry.get().strip()
            if verify_totp_code(secret, code):
                self.add_to_chat("A.R.G.U.S.: CÃ³digo 2FA vÃ¡lido.")
            else:
                self.add_to_chat("A.R.G.U.S.: CÃ³digo 2FA invÃ¡lido.")

        ctk.CTkButton(dialog, text="Salvar segredo", command=save_secret).pack(pady=4)
        ctk.CTkButton(dialog, text="Verificar", command=verify_code).pack()

    def monitoring_loop(self):
        """Loop principal de monitoramento"""
        while self.monitoring:
            try:
                # Coletar dados
                stats = monitor.get_all_stats()
                network_info = network.get_all_network_info()
                alerts = monitor.check_alerts(stats)
                
                # Adicionar ao grÃ¡fico
                graph_manager.add_data_point(
                    stats['cpu'],
                    stats['ram'],
                    stats['gpu'],
                    stats['temperature']
                )
                
                # Log no banco de dados
                db.log_system_stats(
                    stats['cpu'],
                    stats['ram'],
                    stats['gpu'],
                    stats['disk'],
                    stats['temperature'],
                    network_info.get('download_speed', 0),
                    network_info.get('upload_speed', 0),
                    stats['processes']
                )
                
                # Processar alertas
                for alert_type, message in alerts:
                    db.log_alert(alert_type, message, "HIGH")
                    ai.set_system_status("WARNING", message)
                
                # Atualizar UI (usando after para thread-safe)
                self.root.after(0, self.update_ui, stats, network_info)
                
                time.sleep(UPDATE_INTERVAL / 1000)
            except Exception as e:
                print(f"Erro no loop de monitoramento: {e}")
                time.sleep(1)

    def update_ui(self, stats, network_info):
        """Atualiza a UI com os dados coletados"""
        try:
            # Atualizar barras de progresso
            cpu = stats['cpu']
            ram = stats['ram']
            gpu = stats['gpu']
            disk = stats['disk']
            
            self.cpu_progress.set(cpu / 100)
            self.cpu_label.configure(text=f"{cpu:.1f}%")
            
            self.ram_progress.set(ram / 100)
            self.ram_label.configure(text=f"{ram:.1f}%")
            
            self.gpu_progress.set(gpu / 100)
            self.gpu_label.configure(text=f"{gpu:.1f}%")
            
            self.disk_progress.set(disk / 100)
            self.disk_label.configure(text=f"{disk:.1f}%")
            
            # Temperatura
            self.temp_label.configure(text=f"{stats['temperature']:.1f}Â°C")
            
            # Processos
            self.processes_label.configure(text=f"Processos: {stats['processes']}")
            
            # Status
            status_text = "âœ“ NORMAL" if stats['cpu'] < 80 and stats['ram'] < 80 else "âš ï¸ ALERTA"
            self.status_label.configure(text=f"Status: {status_text}")
            
            # Footer com info de rede
            ip = network_info['public_ip']
            speed_down = network_info['download_speed']
            speed_up = network_info['upload_speed']
            city = network_info['city']
            
            footer_text = f"IP: {ip} | Download: {speed_down:.1f} Mbps | Upload: {speed_up:.1f} Mbps | {city}"
            self.footer_label.configure(text=footer_text)
            
        except Exception as e:
            print(f"Erro ao atualizar UI: {e}")

    def on_closing(self):
        """Ao fechar a janela"""
        self.monitoring = False
        if webcam.is_recording:
            webcam.stop_recording()
        self.root.destroy()


def main():
    root = ctk.CTk()
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()



