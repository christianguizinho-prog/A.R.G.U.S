"""
Setup e instalação - A.R.G.U.S.
Script para facilitar a instalação
"""

import os
import subprocess
import sys
import platform


def print_header():
    print("""
    ╔════════════════════════════════════════════╗
    ║   A.R.G.U.S. v3.0 - SETUP INSTALLER      ║
    ║                                            ║
    ║   Sistema Avançado de Reconhecimento,     ║
    ║   Gerenciamento e Vigilância              ║
    ╚════════════════════════════════════════════╝
    """)


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("[1/4] Verificando versão do Python...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
    else:
        print(f"✗ Python 3.8+ necessário (encontrado {version.major}.{version.minor})")
        return False


def create_directories():
    """Cria os diretórios necessários"""
    print("\n[2/4] Criando diretórios...")
    
    dirs = ['assets', 'database']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✓ Diretório '{dir_name}' criado")
        else:
            print(f"✓ Diretório '{dir_name}' já existe")


def install_dependencies():
    """Instala as dependências"""
    print("\n[3/4] Instalando dependências...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao instalar dependências: {e}")
        return False


def verify_installation():
    """Verifica se tudo foi instalado corretamente"""
    print("\n[4/4] Verificando instalação...")
    
    required_modules = [
        'customtkinter',
        'psutil',
        'matplotlib',
        'requests',
        'cv2',  # opencv
        'sqlite3'  # nativo
    ]
    
    missing = []
    for module in required_modules:
        try:
            if module == 'sqlite3':
                import sqlite3
            else:
                __import__(module)
            print(f"✓ {module} ok")
        except ImportError:
            print(f"✗ {module} não encontrado")
            missing.append(module)
    
    return len(missing) == 0


def main():
    print_header()
    
    # Verificar Python
    if not check_python_version():
        print("\n✗ Instalação cancelada")
        return False
    
    # Criar diretórios
    create_directories()
    
    # Instalar dependências
    if not install_dependencies():
        print("\n✗ Erro durante instalação")
        return False
    
    # Verificar
    if verify_installation():
        print("\n" + "="*46)
        print("✓ A.R.G.U.S. instalado com sucesso!")
        print("="*46)
        print("\nPara iniciar, execute:")
        print("  python main.py")
        print("\n")
        return True
    else:
        print("\n⚠️ Algumas dependências podem estar faltando")
        print("Tente executar: pip install -r requirements.txt")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
