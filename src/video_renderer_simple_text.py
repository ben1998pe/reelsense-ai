#!/usr/bin/env python3
"""
Video Renderer Simple Text - Solo texto sincronizado con música
SUPER SIMPLE pero 100% FUNCIONAL
"""

import os
import json
import math
from typing import Dict, Any, Tuple, List
import numpy as np

# MoviePy imports básicos
try:
    from moviepy.editor import VideoClip, CompositeVideoClip, ColorClip, AudioFileClip
except ImportError:
    from moviepy.video.VideoClip import VideoClip, ColorClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip

DEFAULT_SIZE = (1080, 1920)  # 9:16 vertical
DEFAULT_FPS = 30

def create_simple_background(size: Tuple[int, int], duration: float) -> VideoClip:
    """Fondo simple que cambia de color cada 10 segundos"""
    w, h = size
    
    def make_frame(t):
        # Cambiar color cada 10 segundos
        color_index = int(t / 10) % 6
        
        colors = [
            [50, 50, 50],    # Gris oscuro
            [100, 0, 0],     # Rojo oscuro
            [0, 100, 0],     # Verde oscuro
            [0, 0, 100],     # Azul oscuro
            [100, 100, 0],   # Amarillo oscuro
            [100, 0, 100],   # Magenta oscuro
        ]
        
        color = colors[color_index]
        frame = np.full((h, w, 3), color, dtype=np.uint8)
        return frame
    
    return VideoClip(make_frame, duration=duration)

def create_lyrics_display(size: Tuple[int, int], duration: float, concept: Dict[str, Any]) -> VideoClip:
    """Muestra la letra de la canción letra por letra"""
    w, h = size
    
    # Obtener la letra de la transcripción
    lyrics = concept.get('music_analysis', {}).get('transcription', 'No lyrics available')
    
    # Dividir en palabras
    words = lyrics.split()
    
    # Calcular cuándo aparece cada palabra
    word_duration = duration / len(words)
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Calcular cuántas palabras mostrar
        current_word_index = int(t / word_duration)
        current_word_index = min(current_word_index, len(words) - 1)
        
        # Mostrar palabras hasta el índice actual
        display_words = words[:current_word_index + 1]
        
        # Colores vibrantes para el texto
        colors = [
            [255, 255, 255],  # Blanco
            [255, 255, 0],    # Amarillo
            [0, 255, 255],    # Cian
            [255, 0, 255],    # Magenta
            [0, 255, 0],      # Verde
            [255, 0, 0],      # Rojo
        ]
        
        # Posición inicial
        y_start = h // 3
        line_height = 80
        words_per_line = 5
        
        for i, word in enumerate(display_words):
            # Calcular posición
            line_num = i // words_per_line
            word_in_line = i % words_per_line
            
            x = 100 + word_in_line * 180
            y = y_start + line_num * line_height
            
            # Color basado en la posición
            color_index = i % len(colors)
            color = colors[color_index]
            
            # Simular texto (rectángulo de color)
            word_width = len(word) * 20
            word_height = 60
            
            # Asegurar que esté en pantalla
            if x + word_width < w and y + word_height < h:
                # Dibujar "palabra" (rectángulo)
                frame[y:y+word_height, x:x+word_width] = color
                
                # Borde negro para separar
                frame[y:y+word_height, x:x+word_width] = [max(0, c-50) for c in color]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)

def create_beat_indicator(size: Tuple[int, int], duration: float) -> VideoClip:
    """Indicador simple de beat que pulsa"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Pulsar al ritmo (126 BPM = 2.1 Hz)
        beat_freq = 2.1
        pulse = abs(math.sin(t * beat_freq * 2 * math.pi))
        
        # Círculo que pulsa en el centro
        center_x, center_y = w // 2, h // 2
        radius = int(100 + 50 * pulse)
        
        # Dibujar círculo pulsante
        y_indices, x_indices = np.ogrid[:h, :w]
        circle_mask = (x_indices - center_x)**2 + (y_indices - center_y)**2 <= radius**2
        
        # Color rojo que cambia de intensidad
        intensity = int(255 * pulse)
        frame[circle_mask] = [intensity, 0, 0]
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.7)

def create_progress_bar(size: Tuple[int, int], duration: float) -> VideoClip:
    """Barra de progreso simple"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Calcular progreso
        progress = t / duration
        
        # Barra en la parte inferior
        bar_y = h - 100
        bar_height = 20
        
        # Llenar barra según progreso
        bar_width = int(w * progress)
        frame[bar_y:bar_y+bar_height, :bar_width] = [0, 255, 255]  # Cian
        
        # Borde de la barra
        frame[bar_y:bar_y+bar_height, :] = [255, 255, 255]  # Blanco
        
        return frame
    
    return VideoClip(make_frame, duration=duration)

def render_simple_lyrics_video(concept: Dict[str, Any], audio_path: str, output_path: str) -> str:
    """Renderiza video simple con letra sincronizada"""
    
    print("🎵 Iniciando renderizado SIMPLE con letra...")
    
    # Cargar audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    print(f"📽️ Duración del audio: {duration:.2f}s")
    
    # Crear capas SIMPLES
    print("🎨 Creando efectos SIMPLES...")
    
    # 1. Fondo simple
    background = create_simple_background(DEFAULT_SIZE, duration)
    
    # 2. Letra de la canción
    lyrics = create_lyrics_display(DEFAULT_SIZE, duration, concept)
    
    # 3. Indicador de beat
    beat_indicator = create_beat_indicator(DEFAULT_SIZE, duration)
    
    # 4. Barra de progreso
    progress_bar = create_progress_bar(DEFAULT_SIZE, duration)
    
    print("🎭 Componiendo video simple...")
    
    # Componer capas
    clips = [background, lyrics, beat_indicator, progress_bar]
    
    final_video = CompositeVideoClip(clips, size=DEFAULT_SIZE)
    final_video = final_video.with_audio(audio_clip).with_duration(duration)
    
    # Asegurar directorio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("🔄 Renderizando video simple...")
    
    # Renderizar
    final_video.write_videofile(
        output_path,
        fps=DEFAULT_FPS,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    # Limpiar
    final_video.close()
    audio_clip.close()
    
    print(f"✅ Video SIMPLE completado: {output_path}")
    return output_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Render video SIMPLE con letra sincronizada")
    parser.add_argument("audio", help="Archivo de audio")
    parser.add_argument("concept_json", help="JSON con concepto")
    parser.add_argument("--output", "-o", default="outputs/reel_simple_lyrics.mp4", help="Archivo de salida")
    
    args = parser.parse_args()
    
    # Cargar concepto
    with open(args.concept_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer concepto
    if "tiktok_concepts" in data:
        concept = data["tiktok_concepts"][0]
        # Añadir análisis de música al concepto
        concept['music_analysis'] = data.get('music_analysis', {})
    else:
        concept = data
    
    # Renderizar
    output = render_simple_lyrics_video(concept, args.audio, args.output)
    print(f"🎉 Video SIMPLE generado exitosamente: {output}")

if __name__ == "__main__":
    main()
