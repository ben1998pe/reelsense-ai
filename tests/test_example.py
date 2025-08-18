#!/usr/bin/env python3
"""
Script de ejemplo para probar el analizador de música.
Este script muestra cómo usar la clase MusicAnalyzer programáticamente.
"""

from music_analyzer import MusicAnalyzer
import json

def test_analyzer():
    """Función de prueba del analizador."""
    print("🧪 PROBANDO ANALIZADOR DE MÚSICA")
    print("=" * 50)
    
    # Crear instancia del analizador
    analyzer = MusicAnalyzer()
    
    # Ejemplo de texto para probar el análisis de sentimiento
    test_texts = [
        "Te amo con todo mi corazón, eres mi felicidad",
        "Estoy triste y deprimido, todo está mal",
        "¡Qué sorpresa tan increíble! Esto es asombroso",
        "Me siento enojado y furioso por lo que pasó",
        "Tengo miedo y ansiedad por el futuro"
    ]
    
    print("\n📝 PROBANDO ANÁLISIS DE SENTIMIENTO:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Texto: '{text}'")
        sentiment = analyzer.analyze_sentiment(text)
        
        print(f"   Sentimiento: {sentiment['sentiment']}")
        print(f"   Polaridad: {sentiment['polarity']:.3f}")
        print(f"   Subjetividad: {sentiment['subjectivity']:.3f}")
        
        if sentiment['emotions']:
            print(f"   Emociones: {', '.join(sentiment['emotions'].keys())}")
        else:
            print("   Emociones: Ninguna detectada")
    
    print("\n" + "=" * 50)
    print("✅ Prueba completada!")
    print("=" * 50)
    
    # Mostrar información sobre cómo usar con archivos de audio
    print("\n📁 PARA USAR CON ARCHIVOS DE AUDIO:")
    print("python music_analyzer.py 'ruta/al/audio.mp3'")
    print("\n💡 CONSEJOS:")
    print("- Usa archivos de audio cortos (30 segundos - 2 minutos)")
    print("- Formatos soportados: MP3, WAV, FLAC, M4A, OGG")
    print("- El primer uso descargará el modelo Whisper (~150MB)")

if __name__ == "__main__":
    test_analyzer()
