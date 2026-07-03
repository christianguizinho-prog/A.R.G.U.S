"""
Gráficos em tempo real - A.R.G.U.S.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
from datetime import datetime
from config import COLORS


class GraphManager:
    def __init__(self, max_points=60):
        self.max_points = max_points
        
        # Deques para armazenar dados (últimos 60 segundos)
        self.cpu_data = deque(maxlen=max_points)
        self.ram_data = deque(maxlen=max_points)
        self.gpu_data = deque(maxlen=max_points)
        self.temp_data = deque(maxlen=max_points)
        self.time_labels = deque(maxlen=max_points)
        
        # Configurar matplotlib com tema escuro
        plt.style.use('dark_background')

    def add_data_point(self, cpu, ram, gpu, temp):
        """Adiciona um ponto de dados aos gráficos"""
        self.cpu_data.append(cpu)
        self.ram_data.append(ram)
        self.gpu_data.append(gpu)
        self.temp_data.append(temp)
        self.time_labels.append(datetime.now().strftime('%H:%M:%S'))

    def create_combined_graph(self):
        """Cria um gráfico combinado de CPU, RAM e GPU"""
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=COLORS['bg_primary'])
        fig.patch.set_facecolor(COLORS['bg_primary'])
        ax.set_facecolor(COLORS['bg_secondary'])
        
        if len(self.cpu_data) > 0:
            x = range(len(self.cpu_data))
            
            ax.plot(x, list(self.cpu_data), label='CPU', color=COLORS['accent_green'], linewidth=2)
            ax.plot(x, list(self.ram_data), label='RAM', color=COLORS['accent_blue'], linewidth=2)
            ax.plot(x, list(self.gpu_data), label='GPU', color=COLORS['accent_yellow'], linewidth=2)
            
            ax.set_ylabel('Uso (%)', color=COLORS['text_primary'])
            ax.set_xlabel('Tempo', color=COLORS['text_primary'])
            ax.set_ylim(0, 100)
            ax.set_title('Monitoramento do Sistema', color=COLORS['accent_green'], fontsize=14, fontweight='bold')
            ax.legend(loc='upper left', facecolor=COLORS['bg_secondary'], edgecolor=COLORS['border'])
            ax.grid(True, alpha=0.3, color=COLORS['border'])
            ax.tick_params(colors=COLORS['text_secondary'])
        
        return fig

    def create_temperature_graph(self):
        """Cria um gráfico de temperatura"""
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=COLORS['bg_primary'])
        fig.patch.set_facecolor(COLORS['bg_primary'])
        ax.set_facecolor(COLORS['bg_secondary'])
        
        if len(self.temp_data) > 0:
            x = range(len(self.temp_data))
            
            ax.plot(x, list(self.temp_data), label='Temperatura', color=COLORS['accent_red'], linewidth=2)
            ax.fill_between(x, list(self.temp_data), alpha=0.3, color=COLORS['accent_red'])
            
            # Linha de alerta
            ax.axhline(y=80, color=COLORS['accent_yellow'], linestyle='--', label='Alerta (80°C)')
            ax.axhline(y=90, color=COLORS['accent_red'], linestyle='--', label='Crítico (90°C)')
            
            ax.set_ylabel('Temperatura (°C)', color=COLORS['text_primary'])
            ax.set_xlabel('Tempo', color=COLORS['text_primary'])
            ax.set_title('Temperatura da CPU', color=COLORS['accent_green'], fontsize=14, fontweight='bold')
            ax.legend(loc='upper left', facecolor=COLORS['bg_secondary'], edgecolor=COLORS['border'])
            ax.grid(True, alpha=0.3, color=COLORS['border'])
            ax.tick_params(colors=COLORS['text_secondary'])
        
        return fig

    def clear_data(self):
        """Limpa todos os dados coletados"""
        self.cpu_data.clear()
        self.ram_data.clear()
        self.gpu_data.clear()
        self.temp_data.clear()
        self.time_labels.clear()


# Instância global
graph_manager = GraphManager()
