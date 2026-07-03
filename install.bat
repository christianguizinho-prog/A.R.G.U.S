@echo off
REM Script de instalação rápida para A.R.G.U.S. (Windows)

echo.
echo ╔════════════════════════════════════════════╗
echo ║   A.R.G.U.S. v3.0 - QUICK INSTALLER      ║
echo ║   Windows Setup Script                     ║
echo ╚════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python não encontrado!
    echo   Por favor, instale Python 3.8+ de: https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python detectado

REM Criar diretórios
if not exist "assets" mkdir assets
if not exist "database" mkdir database
echo ✓ Diretórios criados

REM Criar ambiente virtual
echo.
echo [1/3] Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências
echo [2/3] Instalando dependências...
pip install -r requirements.txt

REM Verificar instalação
echo [3/3] Verificando instalação...
python -c "import customtkinter; import psutil; import matplotlib; import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Algumas dependências podem estar faltando
) else (
    echo ✓ Todas as dependências instaladas
)

echo.
echo ╔════════════════════════════════════════════╗
echo ║   ✓ A.R.G.U.S. pronto para usar!          ║
echo ╚════════════════════════════════════════════╝
echo.
echo Para iniciar:
echo   python main.py
echo.
pause
