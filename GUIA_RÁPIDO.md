# 🚀 GUIA DE INÍCIO RÁPIDO - A.R.G.U.S. v3.0

## ⚡ Iniciar em 3 Passos

### Passo 1: Instalar Dependências

**Windows:**
```bash
install.bat
```

**Linux/macOS:**
```bash
bash install.sh
```

**Manual:**
```bash
pip install -r requirements.txt
```

### Passo 2: Executar a Aplicação

```bash
python main.py
```

### Passo 3: Aproveitar! 🎉

A interface abrirá automaticamente com tema futurista verde e preto.

---

## 🎮 Primeiros Passos

### 1. Explorando o Dashboard

Ao abrir, você verá:
- **Painel Esquerdo**: Estatísticas em tempo real
  - CPU
  - RAM
  - GPU
  - Disco
  - Temperatura
  - Processos em execução
  - Status geral

- **Painel Direito**: Assistente IA
  - Conversa interativa
  - Análise do sistema
  - Recomendações

- **Footer**: Informações de rede
  - IP público
  - Velocidade de internet
  - Localização

### 2. Testando a IA

Digite na caixa de chat:
```
Olá
Como está meu sistema?
Quem é você?
Dica de otimização
```

### 3. Teste de Velocidade

Clique em "Teste de Velocidade" e aguarde (1-5 minutos).

---

## 📊 O Que Você Pode Fazer

### Monitoramento em Tempo Real
- ✅ Acompanhar CPU, RAM, GPU
- ✅ Verificar temperatura
- ✅ Analisar uso de disco
- ✅ Contar processos ativos

### Networking
- ✅ Ver IP público
- ✅ Localização aproximada
- ✅ Velocidade de internet
- ✅ Hostname e MAC address

### IA Conversacional
- ✅ Conversar sobre o sistema
- ✅ Obter recomendações
- ✅ Receber análises
- ✅ Histórico de conversa

### Banco de Dados
- ✅ Histórico automático
- ✅ Alertas registrados
- ✅ Consultar dados antigos
- ✅ Rastrear tendências

---

## 🔧 Configuração Básica

### Abrir arquivo `config.py`

```python
# Mudar cores (tema)
COLORS = {
    'bg_primary': '#0a0e27',      # Fundo
    'accent_green': '#00ff41',     # Cor principal
    # ... mais cores
}

# Ajustar alertas
TEMP_ALERT_THRESHOLD = 80        # °C
CPU_ALERT_THRESHOLD = 90         # %
RAM_ALERT_THRESHOLD = 90         # %

# Velocidade de atualização
UPDATE_INTERVAL = 1000           # ms
```

---

## 📂 Estrutura Importante

```
ARGUS/
├── main.py              ← Execute isso!
├── dashboard.py         ← Interface
├── monitor.py           ← Dados do sistema
├── network.py           ← Dados de rede
├── ai.py                ← IA
├── database.py          ← Banco de dados
├── config.py            ← Configurações
│
├── database/
│   └── logs.db          ← Dados salvos aqui
│
└── assets/              ← Logos e imagens
```

---

## 🐛 Solução de Problemas

### Erro: Módulo não encontrado
```bash
pip install -r requirements.txt
```

### Aplicação lenta
- Reduza `UPDATE_INTERVAL` em `config.py`
- Feche outros programas
- Reinicie a aplicação

### Webcam não funciona
- Verifique se está conectada
- Verifique se OpenCV está instalado
- Feche outros programas usando a câmera

### Teste de velocidade muito lento
- É normal levar 1-5 minutos
- Verifique sua conexão
- Evite usar internet enquanto testa

---

## 💡 Dicas Úteis

### 1. Usar em Segundo Plano
```python
# Em dashboard.py, comentar a linha de GUI
# Deixar apenas o monitoring_loop() rodando
```

### 2. Exportar Dados
```python
from database import db
stats = db.get_latest_stats(limit=1000)
# Processar dados...
```

### 3. Personalizar IA
```python
# Em ai.py
def get_response(self, user_input):
    # Adicionar suas respostas customizadas
```

### 4. Adicionar Novos Gráficos
```python
# Em graphs.py
def create_custom_graph(self):
    # Implementar novo gráfico
```

---

## 🎯 Próximas Funcionalidades

Para versão 3.1:
- [ ] Login com senha
- [ ] Notificações do sistema
- [ ] Exportar para PDF
- [ ] Reconhecimento de voz

---

## 📚 Recursos Adicionais

- **Documentação completa**: Abra `README.md`
- **Exemplos de código**: Veja `examples.py`
- **Melhorias propostas**: Consulte `MELHORIAS.md`
- **Documentação das libs**:
  - CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
  - psutil: https://psutil.readthedocs.io/
  - matplotlib: https://matplotlib.org/

---

## 🎨 Personalização Rápida

### Mudar Cor Principal
Em `config.py`:
```python
'accent_green': '#00ff41'  # Verde neon
'accent_green': '#00aa00'  # Verde escuro
'accent_green': '#ff0055'  # Rosa/vermelho
'accent_green': '#00aaff'  # Azul claro
```

### Aumentar Frequência de Atualização
```python
UPDATE_INTERVAL = 500  # Meio segundo
```

### Mudar Tema de Cores
```python
# Tema Cyberpunk
COLORS = {
    'bg_primary': '#0d0221',
    'accent_green': '#e0f01d',
    # ...
}
```

---

## 📞 Suporte e Dúvidas

Verificar em ordem:
1. Este arquivo (GUIA_RÁPIDO.md)
2. README.md - Documentação completa
3. examples.py - Exemplos de código
4. Comentários no código fonte

---

## ✅ Checklist para Primeiro Uso

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Executou `python main.py`
- [ ] Interface abriu com tema escuro
- [ ] Dashboard mostrando estatísticas
- [ ] Chat com IA responsivo
- [ ] Teste de velocidade funcionou (opcional)

---

**Pronto para impressionar! 🚀**

Versão: 3.0
Data: 2024
Status: Estável e funcional

**Divirta-se explorando o A.R.G.U.S.!**
