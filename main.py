#!/usr/bin/env python3
"""
Sistema de Adivinhação Baseado em Árvore de Decisão
Inspirado no Akinator - Versão com Interface Gráfica
"""

import sys
import os

def main():
    """Função principal"""
    try:
        # Tenta importar a GUI
        from gui_main import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Erro ao carregar interface gráfica: {e}")
        print("\nCertifique-se de que:")
        print("1. O arquivo gui_main.py está na mesma pasta")
        print("2. Você tem Python 3 com Tkinter instalado")
        print("\nNo Ubuntu/Debian, instale o Tkinter:")
        print("sudo apt-get install python3-tk")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
