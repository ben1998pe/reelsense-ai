#!/usr/bin/env python3
"""
Script de prueba para el analizador de música
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from music_analyzer_improved import ImprovedMusicAnalyzer

def test_sentiment_analysis():
    """Prueba el análisis de sentimiento con textos conocidos."""
    print("🧪 Probando análisis de sentimiento...")
    
    analyzer = ImprovedMusicAnalyzer()
    
    # Textos de prueba
    test_texts = [
        "I love this song, it makes me happy!",
        "This is terrible, I hate it.",
        "The music is okay, nothing special.",
        "Fire and passion, burning desire!"
    ]
    
    for text in test_texts:
        print(f"\n📝 Texto: '{text}'")
        sentiment = analyzer.analyze_sentiment_improved(text)
        print(f"   Sentimiento: {sentiment['sentiment']}")
        print(f"   Polaridad: {sentiment['polarity']:.3f}")
        print(f"   Emociones: {sentiment['emotions']}")

def test_audio_features():
    """Prueba el análisis de características de audio."""
    print("\n🔍 Probando análisis de características de audio...")
    
    # Crear audio de prueba simple
    import numpy as np
    import soundfile as sf
    
    # Generar 5 segundos de audio de prueba
    sample_rate = 44100
    duration = 5
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = 0.3 * np.sin(2 * np.pi * 440 * t)  # Nota A4
    
    # Guardar audio de prueba
    test_audio_path = "test_audio.wav"
    sf.write(test_audio_path, audio, sample_rate)
    
    try:
        analyzer = ImprovedMusicAnalyzer()
        features = analyzer._analyze_audio_features(audio, sample_rate)
        
        print(f"✅ Características analizadas:")
        for key, value in features.items():
            print(f"   {key}: {value}")
            
    finally:
        # Limpiar archivo de prueba
        if os.path.exists(test_audio_path):
            os.remove(test_audio_path)

def test_transcription_confidence():
    """Prueba el cálculo de confianza de transcripción."""
    print("\n📊 Probando cálculo de confianza...")
    
    analyzer = ImprovedMusicAnalyzer()
    
    test_texts = [
        "",  # Texto vacío
        "a",  # Una letra
        "the and or",  # Palabras comunes
        "This is a complete sentence with proper English words.",  # Texto completo
        "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"  # Texto largo
    ]
    
    for text in test_texts:
        confidence = analyzer._calculate_transcription_confidence(text)
        print(f"   Texto: '{text[:30]}{'...' if len(text) > 30 else ''}'")
        print(f"   Confianza: {confidence:.1%}")

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DEL ANALIZADOR DE MÚSICA")
    print("=" * 60)
    
    try:
        test_sentiment_analysis()
        test_audio_features()
        test_transcription_confidence()
        
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
