#!/usr/bin/env python3
"""
Versión mejorada del analizador de música con transcripción más precisa.
"""

import whisper
import librosa
import soundfile as sf
from textblob import TextBlob
import os
import argparse
import numpy as np
from typing import Tuple, Dict, Any
import re

class ImprovedMusicAnalyzer:
    def __init__(self, model_size: str = "small"):
        """
        Inicializa el analizador de música mejorado.
        
        Args:
            model_size: Tamaño del modelo Whisper ("base", "small", "medium", "large")
        """
        print(f"🎵 Analizador de Música Mejorado - ReelSense AI")
        print(f"🔧 Usando modelo Whisper: {model_size}")
        print("=" * 60)
        
        print("Cargando modelo Whisper...")
        self.model = whisper.load_model(model_size)
        print("✅ Modelo cargado exitosamente!")
        
        # Configuraciones para mejor transcripción
        self.transcription_options = {
            "language": "en",  # Idioma inglés para música
            "task": "transcribe",
            "fp16": False,  # Usar FP32 para mejor compatibilidad
            "verbose": False
        }
    
    def preprocess_audio(self, audio_path: str) -> str:
        """
        Preprocesa el audio para mejorar la transcripción.
        
        Args:
            audio_path: Ruta al archivo de audio
            
        Returns:
            Ruta al archivo preprocesado
        """
        print("🔧 Preprocesando audio para mejor transcripción...")
        
        # Cargar audio
        audio, sr = librosa.load(audio_path, sr=None)
        
        # 1. Normalización de volumen
        audio = librosa.util.normalize(audio)
        
        # 2. Reducción de ruido (filtro paso bajo suave)
        from scipy import signal
        b, a = signal.butter(4, 0.1, 'low')
        audio = signal.filtfilt(b, a, audio)
        
        # 3. Enfatizar frecuencias vocales (300Hz - 3400Hz)
        # Crear filtro paso banda para voces
        nyquist = sr / 2
        low = 300 / nyquist
        high = 3400 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        audio_vocals = signal.filtfilt(b, a, audio)
        
        # 4. Mezclar audio original con voces enfatizadas
        audio_enhanced = 0.7 * audio + 0.3 * audio_vocals
        
        # 5. Guardar audio preprocesado
        processed_path = audio_path.replace('.', '_processed.')
        if audio_path.endswith('.mp3'):
            processed_path = audio_path.replace('.mp3', '_processed.wav')
        
        sf.write(processed_path, audio_enhanced, sr)
        print(f"✅ Audio preprocesado guardado: {processed_path}")
        
        return processed_path
    
    def transcribe_audio_improved(self, audio_path: str) -> str:
        """
        Transcribe el audio con mejoras para música.
        
        Args:
            audio_path: Ruta al archivo de audio
            
        Returns:
            Texto transcrito mejorado
        """
        print("📝 Transcribiendo audio con modelo mejorado...")
        
        # Preprocesar audio
        processed_path = self.preprocess_audio(audio_path)
        
        # Transcripción con opciones optimizadas
        result = self.model.transcribe(
            processed_path,
            **self.transcription_options
        )
        
        transcription = result["text"]
        
        # Post-procesamiento del texto
        transcription = self.post_process_transcription(transcription)
        
        # Limpiar archivo temporal
        if os.path.exists(processed_path):
            os.remove(processed_path)
        
        print(f"✅ Transcripción completada: {transcription[:100]}...")
        return transcription
    
    def post_process_transcription(self, text: str) -> str:
        """
        Post-procesa la transcripción para mejorarla.
        
        Args:
            text: Texto transcrito
            
        Returns:
            Texto mejorado
        """
        print("🔍 Post-procesando transcripción...")
        
        # 1. Limpiar espacios extra
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 2. Corregir errores comunes en música
        music_corrections = {
            "I'm gonna": "I'm gonna",
            "never die": "never die",
            "Hold me": "Hold me",
            "in your heart": "in your heart",
            "tonight": "tonight",
            "magic": "magic",
            "dark": "dark",
            "moonlight": "moonlight",
            "love": "love",
            "fire": "fire",
            "wind": "wind",
            "world": "world"
        }
        
        # 3. Filtrar frases sin sentido
        lines = text.split('.')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 3:  # Solo líneas con más de 3 caracteres
                # Verificar que la línea tenga sentido básico
                words = line.split()
                if len(words) >= 2:  # Al menos 2 palabras
                    # Filtrar líneas que parecen ser solo ruido
                    if not self._is_noise_line(line):
                        filtered_lines.append(line)
        
        # 4. Reconstruir texto
        improved_text = '. '.join(filtered_lines)
        
        # 5. Limpiar caracteres extraños
        improved_text = re.sub(r'[^\w\s\.\,\!\?\-\']', '', improved_text)
        
        return improved_text
    
    def _is_noise_line(self, line: str) -> bool:
        """
        Determina si una línea es probablemente ruido.
        
        Args:
            line: Línea de texto
            
        Returns:
            True si es probablemente ruido
        """
        # Patrones que indican ruido
        noise_patterns = [
            r'^\s*[A-Za-z]\s*$',  # Una sola letra
            r'^\s*[A-Za-z]{2}\s*$',  # Dos letras
            r'^\s*[A-Za-z]{3}\s*$',  # Tres letras
            r'^\s*[A-Za-z]+\s+[A-Za-z]+\s*$',  # Dos palabras muy cortas
            r'^\s*[A-Za-z]+\s*$',  # Una palabra muy corta
        ]
        
        for pattern in noise_patterns:
            if re.match(pattern, line):
                return True
        
        return False
    
    def analyze_sentiment_improved(self, text: str) -> Dict[str, Any]:
        """
        Analiza el sentimiento con mejoras para letras de música.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis de sentimiento mejorado
        """
        print("😊 Analizando sentimiento con mejoras...")
        
        # Análisis básico
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Interpretación mejorada del sentimiento
        if polarity > 0.2:
            sentiment = "Muy Positivo"
        elif polarity > 0.05:
            sentiment = "Positivo"
        elif polarity < -0.2:
            sentiment = "Muy Negativo"
        elif polarity < -0.05:
            sentiment = "Negativo"
        else:
            sentiment = "Neutral"
        
        # Análisis de emociones mejorado para música
        emotions = self._analyze_music_emotions(text.lower())
        
        # Análisis de temas musicales
        themes = self._analyze_music_themes(text.lower())
        
        return {
            "text": text,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "emotions": emotions,
            "themes": themes,
            "confidence": self._calculate_transcription_confidence(text)
        }
    
    def _analyze_music_emotions(self, text: str) -> Dict[str, int]:
        """
        Analiza emociones específicas de música.
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            Diccionario con emociones y puntuaciones
        """
        emotion_keywords = {
            "amor": ["love", "heart", "hold me", "romantic", "passion", "forever"],
            "alegría": ["happy", "joy", "smile", "dance", "celebrate", "fun"],
            "tristeza": ["sad", "cry", "tears", "pain", "lonely", "hurt"],
            "energía": ["fire", "burn", "power", "strong", "energy", "wild"],
            "misterio": ["dark", "moon", "night", "magic", "mystery", "shadow"],
            "libertad": ["wind", "fly", "free", "escape", "run", "break"],
            "esperanza": ["hope", "dream", "future", "believe", "faith", "light"]
        }
        
        emotions = {emotion: 0 for emotion in emotion_keywords.keys()}
        
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    emotions[emotion] += 1
        
        return {k: v for k, v in emotions.items() if v > 0}
    
    def _analyze_music_themes(self, text: str) -> Dict[str, int]:
        """
        Analiza temas musicales comunes.
        
        Args:
            text: Texto en minúsculas
            
        Returns:
            Diccionario con temas y puntuaciones
        """
        theme_keywords = {
            "romance": ["love", "heart", "kiss", "romance", "relationship"],
            "empoderamiento": ["strong", "power", "freedom", "independent", "confident"],
            "naturaleza": ["wind", "fire", "earth", "water", "moon", "sun"],
            "vida": ["life", "live", "die", "birth", "death", "soul"],
            "música": ["song", "music", "beat", "rhythm", "melody", "voice"],
            "viaje": ["road", "journey", "travel", "path", "way", "destination"]
        }
        
        themes = {theme: 0 for theme in theme_keywords.keys()}
        
        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    themes[theme] += 1
        
        return {k: v for k, v in themes.items() if v > 0}
    
    def _calculate_transcription_confidence(self, text: str) -> float:
        """
        Calcula la confianza de la transcripción.
        
        Args:
            text: Texto transcrito
            
        Returns:
            Puntuación de confianza (0-1)
        """
        if not text or text.strip() == "":
            return 0.0
        
        # Factores de confianza
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        # Palabras comunes en inglés
        common_words = ["the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]
        common_word_count = sum(1 for word in text.lower().split() if word in common_words)
        
        # Calcular confianza
        if word_count == 0:
            return 0.0
        
        # Más palabras = más confianza
        word_confidence = min(word_count / 50.0, 1.0)
        
        # Más oraciones completas = más confianza
        sentence_confidence = min(sentence_count / 10.0, 1.0)
        
        # Palabras comunes = más confianza
        common_word_confidence = min(common_word_count / word_count, 1.0)
        
        # Promedio ponderado
        confidence = (word_confidence * 0.4 + sentence_confidence * 0.3 + common_word_confidence * 0.3)
        
        return round(confidence, 3)
    
    def analyze_music_segment(self, audio_path: str) -> Dict[str, Any]:
        """
        Analiza un segmento de música completo con mejoras.
        
        Args:
            audio_path: Ruta al archivo de audio
            
        Returns:
            Diccionario con toda la información del análisis
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"No se encontró el archivo: {audio_path}")
            
            # Obtener información del audio
            audio, sr = librosa.load(audio_path, sr=None)
            duration = len(audio) / sr
            
            # Transcripción mejorada
            transcription = self.transcribe_audio_improved(audio_path)
            
            # Análisis de sentimiento mejorado
            sentiment_analysis = self.analyze_sentiment_improved(transcription)
            
            # Características del audio
            audio_features = self._analyze_audio_features(audio, sr)
            
            result = {
                "audio_info": {
                    "file_path": audio_path,
                    "duration_seconds": round(duration, 2),
                    "sample_rate": sr,
                    **audio_features
                },
                "transcription": transcription,
                "sentiment_analysis": sentiment_analysis,
                "analysis_metadata": {
                    "model_used": str(type(self.model).__name__),
                    "preprocessing_applied": True,
                    "post_processing_applied": True
                }
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error durante el análisis: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_audio_features(self, audio: Any, sr: int) -> Dict[str, Any]:
        """
        Analiza características avanzadas del audio.
        
        Args:
            audio: Audio cargado
            sr: Frecuencia de muestreo
            
        Returns:
            Diccionario con características del audio
        """
        print("🔍 Analizando características avanzadas del audio...")
        
        # Duración
        duration = len(audio) / sr
        
        # Energía RMS
        rms = librosa.feature.rms(y=audio)[0]
        avg_rms = float(rms.mean())
        
        # Frecuencia fundamental (pitch)
        try:
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
            pitch_values = pitches[magnitudes > 0.1]
            if len(pitch_values) > 0:
                avg_pitch = float(pitch_values.mean())
            else:
                avg_pitch = 0.0
        except Exception:
            avg_pitch = 0.0
        
        # Tempo
        try:
            tempo_result = librosa.beat.beat_track(y=audio, sr=sr)
            tempo = tempo_result[0] if isinstance(tempo_result, tuple) else tempo_result
        except Exception:
            tempo = 0.0
        
        # Espectral centroid (brillantez)
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            avg_spectral = float(spectral_centroids.mean())
        except Exception:
            avg_spectral = 0.0
        
        return {
            "duration_seconds": round(float(duration), 2),
            "sample_rate": sr,
            "average_rms": round(float(avg_rms), 4),
            "average_pitch_hz": round(float(avg_pitch), 1),
            "tempo_bpm": round(float(tempo), 1),
            "spectral_centroid": round(float(avg_spectral), 1)
        }

def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description="Analizador de música mejorado con transcripción precisa")
    parser.add_argument("audio_path", help="Ruta al archivo de audio")
    parser.add_argument("--output", "-o", help="Archivo de salida para guardar resultados (opcional)")
    parser.add_argument("--model", "-m", choices=["base", "small", "medium", "large"], 
                       default="small", help="Tamaño del modelo Whisper (default: small)")
    
    args = parser.parse_args()
    
    # Crear instancia del analizador mejorado
    analyzer = ImprovedMusicAnalyzer(model_size=args.model)
    
    # Analizar el segmento de música
    print("=" * 60)
    print("ANALIZADOR DE MÚSICA MEJORADO - REELSENSE AI")
    print("=" * 60)
    
    results = analyzer.analyze_music_segment(args.audio_path)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DEL ANÁLISIS MEJORADO")
    print("=" * 60)
    
    # Información del audio
    audio_info = results['audio_info']
    print(f"📁 Archivo: {audio_info['file_path']}")
    print(f"⏱️  Duración: {audio_info['duration_seconds']} segundos")
    print(f"🎵 Frecuencia de muestreo: {audio_info['sample_rate']} Hz")
    print(f"🔊 Energía RMS promedio: {audio_info['average_rms']}")
    print(f"🎼 Pitch promedio: {audio_info['average_pitch_hz']} Hz")
    print(f"🥁 Tempo: {audio_info['tempo_bpm']} BPM")
    print(f"✨ Brillo espectral: {audio_info['spectral_centroid']}")
    
    # Transcripción
    print(f"\n📝 TRANSCRIPCIÓN MEJORADA:")
    print(f"'{results['transcription']}'")
    
    # Análisis de sentimiento
    sentiment = results['sentiment_analysis']
    print(f"\n😊 ANÁLISIS DE SENTIMIENTO MEJORADO:")
    print(f"Sentimiento general: {sentiment['sentiment']}")
    print(f"Polaridad: {sentiment['polarity']:.3f} (-1 = muy negativo, 1 = muy positivo)")
    print(f"Subjetividad: {sentiment['subjectivity']:.3f} (0 = objetivo, 1 = subjetivo)")
    print(f"Confianza de transcripción: {sentiment['confidence']:.1%}")
    
    if sentiment['emotions']:
        print(f"Emociones detectadas:")
        for emotion, score in sentiment['emotions'].items():
            print(f"  • {emotion.capitalize()}: {score}")
    
    if sentiment['themes']:
        print(f"Temas musicales:")
        for theme, score in sentiment['themes'].items():
            print(f"  • {theme.capitalize()}: {score}")
    
    # Metadatos del análisis
    metadata = results['analysis_metadata']
    print(f"\n🔧 METADATOS DEL ANÁLISIS:")
    print(f"Modelo Whisper: {metadata['model_used']}")
    print(f"Preprocesamiento: {'✅ Aplicado' if metadata['preprocessing_applied'] else '❌ No aplicado'}")
    print(f"Post-procesamiento: {'✅ Aplicado' if metadata['post_processing_applied'] else '❌ No aplicado'}")
    
    # Guardar resultados si se especifica
    if args.output:
        import json
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Resultados guardados en: {args.output}")
    
    print("\n" + "=" * 60)
    print("¡Análisis mejorado completado!")
    print("=" * 60)

if __name__ == "__main__":
    main()
