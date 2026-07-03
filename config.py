"""
Configurações do A.R.G.U.S.
"""

# Cores do tema escuro futurista
COLORS = {
    'bg_primary': '#0a0e27',
    'bg_secondary': '#141829',
    'accent_green': '#00ff41',
    'accent_red': '#ff0055',
    'accent_yellow': '#ffaa00',
    'accent_blue': '#00aaff',
    'text_primary': '#ffffff',
    'text_secondary': '#888888',
    'border': '#1a1f3a'
}

# Configurações de atualização
UPDATE_INTERVAL = 1000  # ms

# Limite de temperatura
TEMP_ALERT_THRESHOLD = 80

# Limite de uso de CPU
CPU_ALERT_THRESHOLD = 90

# Limite de RAM
RAM_ALERT_THRESHOLD = 90

# Banco de dados
DB_PATH = 'database/logs.db'

# Tamanho máximo de histórico
MAX_HISTORY = 10000

# Tema
THEME = 'dark'
