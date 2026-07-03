"""
A.R.G.U.S. - Sistema Avançado de Reconhecimento, Gerenciamento e Vigilância
Ponto de entrada principal da aplicação
"""

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard import main


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║        A.R.G.U.S. v3.0                    ║
    ║  Sistema Avançado de Reconhecimento,      ║
    ║  Gerenciamento e Vigilância               ║
    ║                                            ║
    ║  Iniciando interface...                    ║
    ╚════════════════════════════════════════════╝
    """)
    
    try:
        main()
    except Exception as e:
        print(f"Erro ao iniciar A.R.G.U.S.: {e}")
        import traceback
        traceback.print_exc()
