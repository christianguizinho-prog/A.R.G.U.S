"""
Dashboard da interface - A.R.G.U.S.
"""

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkTextbox, CTkEntry, CTkProgressBar
import threading
import time
from datetime import datetime
from config import COLORS, UPDATE_INTERVAL
from monitor import monitor
from network import network
from ai import ai
from database import db
from graphs import graph_manager


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("A.R.G.U.S. v3.0 - Sistema de Monitoramento em Tempo Real")
        self.root.geometry("1400x900")
        self.root.configure(fg_color=COLORS['bg_primary'])
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.monitoring = True
        self.update_thread = None
        
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        """Configura a interface do usuário"""
        # Container principal com scroll
        main_container = CTkFrame(self.root, fg_color=COLORS['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header(main_container)
        
        # Conteúdo principal com duas colunas
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
        
        # Footer
        self.setup_footer(main_container)

    def setup_header(self, parent):
        """Configura o header da aplicação"""
        header = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        header.pack(fill="x", pady=(0, 10))
        
        # Título
        title = CTkLabel(
            header,
            text="🛡️ A.R.G.U.S. v3.0",
            font=("Arial", 28, "bold"),
            text_color=COLORS['accent_green']
        )
        title.pack(pady=15)
        
        subtitle = CTkLabel(
            header,
            text="Sistema Avançado de Reconhecimento, Gerenciamento e Vigilância",
            font=("Arial", 12),
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(pady=(0, 15))

    def setup_monitoring_panel(self, parent):
        """Configura o painel de monitoramento"""
        # Frame do monitoramento
        monitor_frame = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        monitor_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        title = CTkLabel(
            monitor_frame,
            text="📊 MONITORAMENTO DO SISTEMA",
            font=("Arial", 14, "bold"),
            text_color=COLORS['accent_green']
        )
        title.pack(pady=10)
        
        # Área de scroll para os monitores
        scroll_frame = CTkFrame(monitor_frame, fg_color=COLORS['bg_secondary'])
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CPU
        self.create_stat_widget(scroll_frame, "CPU", "cpu_label", "cpu_progress", "cpu_percent")
        
        # RAM
        self.create_stat_widget(scroll_frame, "RAM", "ram_label", "ram_progress", "ram_percent")
        
        # GPU
        self.create_stat_widget(scroll_frame, "GPU", "gpu_label", "gpu_progress", "gpu_percent")
        
        # Disco
        self.create_stat_widget(scroll_frame, "DISCO", "disk_label", "disk_progress", "disk_percent")
        
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
            text="--°C",
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

    def create_stat_widget(self, parent, name, label_id, progress_id, percent_id):
        """Cria um widget de estatística"""
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
            text="🤖 ASSISTENTE A.R.G.U.S.",
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
        
        # Exibir saudação inicial
        greeting = ai.get_greeting()
        self.add_to_chat(f"A.R.G.U.S.: {greeting}")

    def setup_footer(self, parent):
        """Configura o footer"""
        footer = CTkFrame(parent, fg_color=COLORS['bg_secondary'], corner_radius=10)
        footer.pack(fill="x")
        
        # Informações de rede
        info_text = CTkLabel(
            footer,
            text="IP: -- | Velocidade: -- Mbps | Status: Conectando...",
            font=("Arial", 10),
            text_color=COLORS['text_secondary']
        )
        info_text.pack(pady=10)
        
        self.footer_label = info_text
        
        # Botões de ação
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

    def send_message(self, event=None):
        """Envia uma mensagem para a IA"""
        message = self.input_field.get().strip()
        
        if message:
            self.add_to_chat(f"Você: {message}")
            self.input_field.delete(0, "end")
            
            # Gerar resposta
            response = ai.get_response(message)
            self.add_to_chat(f"A.R.G.U.S.: {response}")
            
            # Adicionar ao histórico
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
                message = f"Teste concluído!\nDownload: {result['download']:.2f} Mbps\nUpload: {result['upload']:.2f} Mbps"
                self.add_to_chat(f"A.R.G.U.S.: {message}")
            else:
                self.add_to_chat("A.R.G.U.S.: Erro ao executar teste de velocidade.")
        
        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def start_monitoring(self):
        """Inicia o thread de monitoramento"""
        self.update_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.update_thread.start()

    def monitoring_loop(self):
        """Loop principal de monitoramento"""
        while self.monitoring:
            try:
                # Coletar dados
                stats = monitor.get_all_stats()
                network_info = network.get_all_network_info()
                alerts = monitor.check_alerts()
                
                # Adicionar ao gráfico
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
            self.temp_label.configure(text=f"{stats['temperature']:.1f}°C")
            
            # Processos
            self.processes_label.configure(text=f"Processos: {stats['processes']}")
            
            # Status
            status_text = "✓ NORMAL" if stats['cpu'] < 80 and stats['ram'] < 80 else "⚠️ ALERTA"
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
        self.root.destroy()


def main():
    root = ctk.CTk()
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
