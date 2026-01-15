#!/usr/bin/env python3
"""
Punto de entrada principal del Sistema de Cálculo de Bombeo.

Este módulo configura el path del proyecto e inicia la aplicación GUI
para el cálculo de sistemas de bombeo hidráulico.

Author: Proyecto Nay
Version: 1.0
"""

import sys
import os

# Agregar el directorio src al path de Python para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui import main


if __name__ == "__main__":
    main()
