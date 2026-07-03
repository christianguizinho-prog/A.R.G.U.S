#!/bin/bash
# Script de instalação para A.R.G.U.S. (Linux/macOS)

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   A.R.G.U.S. v3.0 - QUICK INSTALLER      ║"
echo "║   Linux/macOS Setup Script                 ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 não encontrado!"
    echo "  Por favor, instale Python 3.8+ primeiro"
    exit 1
fi

echo "✓ Python detectado: $(python3 --version)"

# Criar diretórios
mkdir -p assets database
echo "✓ Diretórios criados"

# Criar ambiente virtual
echo ""
echo "[1/3] Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "[2/3] Instalando dependências..."
pip install -r requirements.txt

# Verificar instalação
echo "[3/3] Verificando instalação..."
python3 -c "import customtkinter; import psutil; import matplotlib; import requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Todas as dependências instaladas"
else
    echo "⚠️ Algumas dependências podem estar faltando"
fi

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   ✓ A.R.G.U.S. pronto para usar!          ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "Para iniciar:"
echo "  python3 main.py"
echo ""
