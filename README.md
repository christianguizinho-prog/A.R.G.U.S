# 🛡️ A.R.G.U.S. v3.0 - Sistema de Monitoramento em Tempo Real

## 📖 Descrição

**A.R.G.U.S.** (Sistema Avançado de Reconhecimento, Gerenciamento e Vigilância) é um projeto Python avançado que oferece uma interface futurista para monitorar seu computador em tempo real. Combina várias tecnologias para criar uma experiência de monitoramento profissional e visualmente impressionante.

## ✨ Características Principais

- 🖥️ **Monitoramento em Tempo Real**: CPU, GPU, RAM e Disco
- 📊 **Gráficos Dinâmicos**: Visualização de dados em tempo real
- 🌐 **Informações de Rede**: IP público, localização, velocidade de internet
- 🤖 **Assistente IA**: Conversa inteligente sobre o sistema
- 🌙 **Interface Futurista**: Design estilo hacker (verde e preto)
- 🔔 **Sistema de Alertas**: Notificações quando limites são excedidos
- 📁 **Análise de Processos**: Detecta processos suspeitos
- 📈 **Banco de Dados**: Histórico de monitoramento em SQLite
- ⚡ **Atualização em Tempo Real**: Dados atualizados a cada segundo
- 📷 **Suporte a Webcam**: Opcional com autorização do usuário

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|----------|
| **Python** | 3.8+ | Linguagem principal |
| **CustomTkinter** | 5.2.0 | Interface gráfica moderna |
| **psutil** | 5.9.6 | Monitoramento do sistema |
| **matplotlib** | 3.8.2 | Gráficos em tempo real |
| **requests** | 2.31.0 | Requisições HTTP |
| **speedtest-cli** | 1.0.7 | Teste de velocidade |
| **opencv-python** | 4.8.1.78 | Processamento de webcam |
| **sqlite3** | Nativo | Banco de dados |
| **threading/asyncio** | Nativo | Processamento paralelo |

## 📁 Estrutura do Projeto

```
ARGUS/
├── main.py                 # Ponto de entrada
├── dashboard.py            # Interface gráfica principal
├── monitor.py              # Monitoramento do sistema
├── network.py              # Informações de rede
├── ai.py                   # Assistente IA
├── database.py             # Gerenciamento de banco de dados
├── graphs.py               # Gráficos em tempo real
├── webcam.py               # Monitoramento de webcam
├── config.py               # Configurações
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
│
├── assets/                 # Recursos (logos, imagens)
│   ├── logo.png
│   └── background.png
│
└── database/               # Banco de dados
    └── logs.db
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Windows, Linux ou macOS

### Passo 1: Clonar/Preparar o Projeto

```bash
cd ARGUS
```

### Passo 2: Criar Ambiente Virtual (Opcional mas Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Executar a Aplicação

```bash
python main.py
```

## 📊 Interface do Dashboard

```
╔══════════════════════════════════════════╗
║        A.R.G.U.S. v3.0                  ║
║   Sistema de Monitoramento em           ║
║   Tempo Real                             ║
╠══════════════════════════════════════════╣

CPU.............23%
████████░░░░░░░░░░░

RAM.............48%
██████████████░░░░

GPU.............31%
███████████░░░░░░

DISCO...........56%
█████████████░░░░░

Temperatura......56°C

Processos.......198

Status.....✓ NORMAL

═══════════════════════════════════════════

[🤖 ASSISTENTE A.R.G.U.S.]

"Olá! Todos os sistemas operacionais.
Nenhuma atividade suspeita detectada."

[Chat Input Field]
═══════════════════════════════════════════

IP: 191.xxx.xxx.xxx | Download: 523 Mbps
Upload: 211 Mbps | São Paulo
```

## 🔧 Módulos Principais

### `monitor.py`
Coleta informações de CPU, RAM, GPU, temperatura e processos do sistema.

**Funções principais:**
- `get_cpu_usage()` - Uso de CPU
- `get_ram_usage()` - Uso de RAM
- `get_gpu_usage()` - Uso de GPU
- `get_temperature()` - Temperatura da CPU
- `get_suspicious_processes()` - Processos com alto consumo

### `network.py`
Coleta informações de rede e conectividade.

**Funções principais:**
- `get_public_ip()` - IP público
- `get_location()` - Localização aproximada
- `check_internet()` - Verifica conectividade
- `test_speed()` - Teste de velocidade (Speedtest)

### `ai.py`
Assistente IA conversacional que fornece insights sobre o sistema.

**Funções principais:**
- `get_greeting()` - Saudação personalizada
- `analyze_system()` - Análise de desempenho
- `get_response()` - Resposta baseada em entrada do usuário

### `database.py`
Gerencia o armazenamento de histórico em SQLite.

**Tabelas:**
- `system_logs` - Histórico de estatísticas
- `alerts` - Registro de alertas
- `file_events` - Eventos de arquivo
- `network_info` - Informações de rede

### `graphs.py`
Cria gráficos em tempo real com matplotlib.

**Gráficos disponíveis:**
- Combinado: CPU, RAM, GPU
- Temperatura com limites de alerta

### `dashboard.py`
Interface gráfica principal com CustomTkinter.

## ⚙️ Configuração

Edite `config.py` para personalizar:

```python
# Cores do tema
COLORS = {
    'bg_primary': '#0a0e27',
    'accent_green': '#00ff41',
    # ... mais cores
}

# Limites de alerta
TEMP_ALERT_THRESHOLD = 80
CPU_ALERT_THRESHOLD = 90
RAM_ALERT_THRESHOLD = 90

# Intervalo de atualização (em ms)
UPDATE_INTERVAL = 1000
```

## 🎮 Como Usar

1. **Monitoramento Automático**: Inicie o programa e todos os dados serão atualizados automaticamente
2. **Chat com IA**: Digite mensagens na caixa de entrada para conversar
3. **Teste de Velocidade**: Clique em "Teste de Velocidade" para medir sua internet
4. **Alertas**: Receba notificações quando valores excederem limites
5. **Histórico**: Todos os dados são salvos no banco de dados

## 📈 Funcionalidades Avançadas

### Análise de Processos Suspeitos

```python
suspicious = monitor.get_suspicious_processes()
# Retorna: [{'name': 'process.exe', 'pid': 1234, 'cpu': 75.5, 'memory': 12.3}]
```

### Log de Alertas

```python
db.log_alert('CPU_ALTA', 'Uso de CPU excedeu 90%', 'HIGH')
```

### Consultar Histórico

```python
stats = db.get_latest_stats(limit=100)
```

## 🎨 Personalização

### Mudar Tema de Cores

Edit `config.py`:

```python
COLORS = {
    'bg_primary': '#0a0e27',      # Fundo principal
    'accent_green': '#00ff41',     # Cor de destaque
    'accent_red': '#ff0055',       # Cor de alerta
    # ... mais cores
}
```

### Ajustar Temas de Alerta

```python
TEMP_ALERT_THRESHOLD = 80    # Temperatura crítica
CPU_ALERT_THRESHOLD = 90     # CPU crítica
RAM_ALERT_THRESHOLD = 90     # RAM crítica
```

## 🐛 Troubleshooting

### Erro: "psutil não encontrado"
```bash
pip install psutil
```

### Erro: "CustomTkinter não encontrado"
```bash
pip install customtkinter
```

### Erro: "Webcam não funciona"
Verifique se:
1. Sua câmera está conectada
2. Não há outro programa usando a webcam
3. OpenCV está instalado: `pip install opencv-python`

### Erro: "Speedtest muito lento"
O teste de velocidade pode levar 1-5 minutos. Seja paciente!

## 🚀 Próximas Melhorias

- [ ] Login com autenticação
- [ ] Exportação para PDF/Excel
- [ ] Modo tela cheia
- [ ] Notificações do sistema
- [ ] Comandos por voz
- [ ] Automação de tarefas
- [ ] Dashboard na web
- [ ] Suporte a múltiplas idiomas

## 📊 Exemplo de Uso em Código

```python
from monitor import monitor
from network import network
from database import db
from ai import ai

# Obter estatísticas
stats = monitor.get_all_stats()
print(f"CPU: {stats['cpu']}%")
print(f"RAM: {stats['ram']}%")

# Obter informações de rede
net_info = network.get_all_network_info()
print(f"IP: {net_info['public_ip']}")

# Consultar histórico
history = db.get_latest_stats(limit=50)

# Usar IA
response = ai.get_response("Como está meu sistema?")
print(response)
```

## 📝 Licença

Este projeto é fornecido como está, para fins educacionais e pessoais.

## 🤝 Contribuições

Sinta-se livre para:
- Adicionar novas funcionalidades
- Melhorar a interface
- Corrigir bugs
- Sugerir melhorias

## 📧 Suporte

Para problemas, perguntas ou sugestões, verifique:
1. O arquivo README
2. Os comentários no código
3. A documentação das bibliotecas utilizadas

## ⭐ Nivel do Projeto

**Avançado** ⭐⭐⭐⭐⭐

Este projeto demonstra:
- ✅ Interfaces gráficas modernas (CustomTkinter)
- ✅ Multithreading e processamento paralelo
- ✅ Banco de dados (SQLite)
- ✅ Integração com APIs (IP, Localização, Speedtest)
- ✅ Monitoramento de sistema (psutil)
- ✅ Visualização de dados (matplotlib)
- ✅ Arquitetura modular e escalável
- ✅ IA conversacional simples

---

**Desenvolvido com ❤️ para impressionar em portfólios e demonstrações**

Versão: 3.0
Última atualização: 20