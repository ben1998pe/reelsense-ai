#!/usr/bin/env python3
"""
Video Renderer FIXED - Genera reels TikTok con animaciones reales
"""

import os
import json
import math
import random
from typing import Dict, Any, Tuple, List
import numpy as np

# MoviePy imports
try:
    from moviepy.editor import *
except ImportError:
    from moviepy.video.VideoClip import VideoClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.video.VideoClip import ColorClip, TextClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip

# Pillow para texto
from PIL import Image, ImageDraw, ImageFont

DEFAULT_SIZE = (1080, 1920)  # 9:16 vertical
DEFAULT_FPS = 30

def create_gradient_background(size: Tuple[int, int], duration: float, colors: List[Tuple[int, int, int]]) -> VideoClip:
    """Crea un fondo degradado animado"""
    w, h = size
    
    def make_frame(t):
        # Crear gradiente que cambia con el tiempo
        progress = (t / duration) % 1.0
        
        # Interpolar entre colores
        color_idx = int(progress * len(colors))
        next_idx = (color_idx + 1) % len(colors)
        
        color1 = np.array(colors[color_idx])
        color2 = np.array(colors[next_idx])
        
        # Factor de interpolación
        factor = (progress * len(colors)) % 1.0
        
        # Crear gradiente vertical
        gradient = np.zeros((h, w, 3), dtype=np.uint8)
        for y in range(h):
            ratio = y / h
            # Mezclar colores basado en posición Y y tiempo
            final_color = color1 * (1 - ratio) + color2 * ratio
            final_color = final_color * (1 - factor) + color2 * factor
            gradient[y, :] = np.clip(final_color, 0, 255)
        
        return gradient
    
    return VideoClip(make_frame, duration=duration)

def create_typewriter_effect(text: str, size: Tuple[int, int], start_time: float, typing_duration: float) -> List[VideoClip]:
    """Crea efecto de máquina de escribir"""
    if not text:
        return []
    
    # Limpiar texto
    text = text[:100]  # Limitar longitud
    
    clips = []
    chars_per_second = len(text) / typing_duration
    
    for i in range(1, len(text) + 1):
        partial_text = text[:i]
        appear_time = start_time + (i - 1) / chars_per_second
        
        try:
            # Usar TextClip simple
            txt_clip = TextClip(
                partial_text,
                fontsize=60,
                color='white',
                font='Arial-Bold'
            ).set_position('center').set_start(appear_time).set_duration(0.1)
            
            clips.append(txt_clip)
        except:
            # Fallback sin fuente específica
            txt_clip = TextClip(
                partial_text,
                fontsize=60,
                color='white'
            ).set_position('center').set_start(appear_time).set_duration(0.1)
            
            clips.append(txt_clip)
    
    return clips

def create_pulsing_text(text: str, size: Tuple[int, int], start_time: float, duration: float) -> VideoClip:
    """Crea texto que pulsa al ritmo"""
    if not text:
        return ColorClip(size, color=(0,0,0), duration=0)
    
    def size_function(t):
        # Pulso cada 0.5 segundos
        pulse = 1 + 0.3 * abs(math.sin(t * 4 * math.pi))
        return pulse
    
    try:
        txt_clip = TextClip(
            text[:80],  # Limitar texto
            fontsize=50,
            color='yellow',
            font='Arial-Bold'
        ).set_position('center').set_start(start_time).set_duration(duration)
        
        # Aplicar efecto de pulso
        txt_clip = txt_clip.resize(size_function)
        
        return txt_clip
    except:
        # Fallback
        return TextClip(
            text[:80],
            fontsize=50,
            color='yellow'
        ).set_position('center').set_start(start_time).set_duration(duration).resize(size_function)

def create_sliding_text(text: str, size: Tuple[int, int], start_time: float, duration: float, direction: str = 'right') -> VideoClip:
    """Crea texto que se desliza"""
    if not text:
        return ColorClip(size, color=(0,0,0), duration=0)
    
    w, h = size
    
    def pos_function(t):
        progress = t / duration
        if direction == 'right':
            x = int(-w + (w * 1.5) * progress)
            return (x, h * 0.7)
        elif direction == 'left':
            x = int(w - (w * 1.5) * progress)
            return (x, h * 0.7)
        else:  # from bottom
            y = int(h - (h * 0.5) * progress)
            return ('center', y)
    
    try:
        txt_clip = TextClip(
            text[:60],
            fontsize=45,
            color='cyan',
            font='Arial-Bold'
        ).set_start(start_time).set_duration(duration)
        
        txt_clip = txt_clip.set_position(pos_function)
        
        return txt_clip
    except:
        return TextClip(
            text[:60],
            fontsize=45,
            color='cyan'
        ).set_start(start_time).set_duration(duration).set_position(pos_function)

def create_beat_visualization(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea visualización de beats simple"""
    w, h = size
    
    def make_frame(t):
        # Crear barras que pulsan
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Simular beats cada 0.5 segundos
        beat_intensity = abs(math.sin(t * 4 * math.pi))
        
        # Dibujar barras en la parte inferior
        bar_height = int(100 * beat_intensity)
        frame[h-bar_height:h, :] = [50, 100, 255]  # Azul
        
        return frame
    
    return VideoClip(make_frame, duration=duration)

def render_wow_reel(concept: Dict[str, Any], audio_path: str, output_path: str, transcription: str = "") -> str:
    """Renderiza un reel con efectos WOW"""
    
    print("🎬 Iniciando renderizado WOW...")
    
    # Cargar audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    print(f"📽️ Duración del audio: {duration:.2f}s")
    
    # Colores para el gradiente (más vibrantes)
    colors = [
        (139, 69, 19),   # Marrón
        (255, 20, 147),  # Rosa fucsia
        (75, 0, 130),    # Índigo
        (255, 140, 0),   # Naranja
        (50, 205, 50)    # Verde lima
    ]
    
    # Crear fondo degradado animado
    background = create_gradient_background(DEFAULT_SIZE, duration, colors)
    
    # Crear visualización de beats
    beat_viz = create_beat_visualization(DEFAULT_SIZE, duration)
    
    clips = [background, beat_viz]
    
    # Extraer información del concepto
    title = concept.get("concept_title", "Amazing Reel")
    hook = concept.get("story_structure", {}).get("hook_moment", "¡Increíble!")
    development = concept.get("story_structure", {}).get("development", "Esto te va a sorprender...")
    climax = concept.get("story_structure", {}).get("climax", "¡WOW!")
    
    # Timeline dividido
    segment_duration = duration / 5
    
    # 1. Título con efecto typewriter (primeros 20%)
    if title:
        typewriter_clips = create_typewriter_effect(title, DEFAULT_SIZE, 0, segment_duration)
        clips.extend(typewriter_clips)
    
    # 2. Hook pulsante (20%-40%)
    if hook:
        hook_clip = create_pulsing_text(hook, DEFAULT_SIZE, segment_duration, segment_duration)
        clips.append(hook_clip)
    
    # 3. Development deslizante (40%-70%)
    if development:
        dev_clip = create_sliding_text(development, DEFAULT_SIZE, segment_duration * 2, segment_duration * 1.5, 'right')
        clips.append(dev_clip)
    
    # 4. Climax explosivo (70%-90%)
    if climax:
        climax_clip = create_pulsing_text(climax, DEFAULT_SIZE, segment_duration * 3.5, segment_duration, )
        clips.append(climax_clip)
    
    # 5. Hashtags finales (últimos 20%)
    hashtags = concept.get("hashtags", [])
    if hashtags:
        hashtag_text = " ".join([f"#{tag.lstrip('#')}" for tag in hashtags[:3]])
        hashtag_clip = create_sliding_text(hashtag_text, DEFAULT_SIZE, segment_duration * 4, segment_duration, 'bottom')
        clips.append(hashtag_clip)
    
    print(f"🎭 Creados {len(clips)} clips de video")
    
    # Componer video final
    final_video = CompositeVideoClip(clips, size=DEFAULT_SIZE)
    final_video = final_video.set_audio(audio_clip).set_duration(duration)
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("🔄 Renderizando video...")
    
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
    
    print(f"✅ Reel WOW completado: {output_path}")
    return output_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Render TikTok reel con efectos WOW")
    parser.add_argument("audio", help="Archivo de audio")
    parser.add_argument("concept_json", help="JSON con concepto")
    parser.add_argument("--output", "-o", default="outputs/reel_wow.mp4", help="Archivo de salida")
    
    args = parser.parse_args()
    
    # Cargar concepto
    with open(args.concept_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer concepto y transcripción
    if "tiktok_concepts" in data:
        concept = data["tiktok_concepts"][0]
        transcription = data.get("music_analysis", {}).get("transcription", "")
    else:
        concept = data
        transcription = ""
    
    # Renderizar
    output = render_wow_reel(concept, args.audio, args.output, transcription)
    print(f"🎉 Reel generado exitosamente: {output}")

if __name__ == "__main__":
    main()

