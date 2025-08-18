#!/usr/bin/env python3
"""
ReelSense AI - Analizador de Música
Script principal para ejecutar el análisis de música.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from music_analyzer_improved import ImprovedMusicAnalyzer, main as analyzer_main

if __name__ == "__main__":
    print("🎵 ReelSense AI - Analizador de Música")
    print("=" * 50)
    print("Ejecutando desde el script principal...")
    print()
    
    # Ejecutar el analizador
    analyzer_main()
