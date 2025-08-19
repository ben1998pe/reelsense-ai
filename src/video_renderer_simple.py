#!/usr/bin/env python3
"""
Video Renderer Simple - Genera reels TikTok con efectos procedurales sin TextClip
"""

import os
import json
import math
import random
from typing import Dict, Any, Tuple, List
import numpy as np

# MoviePy imports
try:
    from moviepy.editor import VideoClip, CompositeVideoClip, ColorClip, AudioFileClip
except ImportError:
    from moviepy.video.VideoClip import VideoClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.video.VideoClip import ColorClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip

DEFAULT_SIZE = (1080, 1920)  # 9:16 vertical
DEFAULT_FPS = 30

def create_dynamic_background(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea un fondo dinámico con ondas y colores"""
    w, h = size
    
    def make_frame(t):
        # Crear patrones ondulados dinámicos
        x = np.linspace(0, 4*np.pi, w)
        y = np.linspace(0, 6*np.pi, h)
        X, Y = np.meshgrid(x, y)
        
        # Ondas que cambian con el tiempo
        wave1 = np.sin(X + t * 2) * np.cos(Y + t * 1.5)
        wave2 = np.cos(X * 2 + t * 3) * np.sin(Y * 1.5 + t * 2)
        combined = (wave1 + wave2) / 2
        
        # Convertir a colores RGB vibrantes
        # Canal rojo: ondas base
        r = np.clip((combined + 1) * 127 + 64, 0, 255)
        # Canal verde: ondas desfasadas
        g = np.clip((np.sin(combined * np.pi + t) + 1) * 127 + 32, 0, 255)
        # Canal azul: patrón circular
        center_x, center_y = w//2, h//2
        dist = np.sqrt((np.arange(w) - center_x)**2 + (np.arange(h)[:, None] - center_y)**2)
        b = np.clip((np.sin(dist/100 + t*4) + 1) * 127 + 64, 0, 255)
        
        # Combinar canales
        frame = np.stack([r, g, b], axis=2).astype(np.uint8)
        
        return frame
    
    return VideoClip(make_frame, duration=duration)

def create_geometric_overlay(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea overlay geométrico animado"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Círculos pulsantes
        center_x, center_y = w//2, h//2
        
        # Círculo principal que pulsa
        pulse = abs(math.sin(t * 4)) * 0.8 + 0.2
        radius = int(200 * pulse)
        
        # Crear múltiples círculos
        for i, (cx, cy) in enumerate([(center_x, center_y//3), (center_x, center_y), (center_x, center_y*4//3)]):
            phase = t * 3 + i * 2
            r = int(150 * (abs(math.sin(phase)) * 0.6 + 0.4))
            
            # Dibujar círculo (aproximación con cuadrados)
            y_indices, x_indices = np.ogrid[:h, :w]
            mask = (x_indices - cx)**2 + (y_indices - cy)**2 <= r**2
            
            # Color basado en el tiempo y posición
            color_r = int(127 * (math.sin(phase) + 1))
            color_g = int(127 * (math.cos(phase + 1) + 1))
            color_b = int(127 * (math.sin(phase + 2) + 1))
            
            frame[mask] = [color_r, color_g, color_b]
        
        # Líneas dinámicas
        line_y = int(h/2 + 200 * math.sin(t * 2))
        if 0 <= line_y < h:
            frame[max(0, line_y-5):min(h, line_y+5), :] = [255, 255, 0]  # Línea amarilla
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.6)

def create_particle_system(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea sistema de partículas animadas"""
    w, h = size
    
    # Generar partículas
    num_particles = 50
    particles = []
    for _ in range(num_particles):
        particles.append({
            'x': random.randint(0, w),
            'y': random.randint(0, h),
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-3, 1),
            'size': random.randint(3, 8),
            'phase': random.uniform(0, 2*math.pi)
        })
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        for p in particles:
            # Actualizar posición
            x = (p['x'] + p['vx'] * t * 30) % w
            y = (p['y'] + p['vy'] * t * 30) % h
            
            # Brillo pulsante
            brightness = int(255 * (math.sin(t * 3 + p['phase']) * 0.4 + 0.6))
            
            # Dibujar partícula
            px, py = int(x), int(y)
            size = p['size']
            
            # Crear máscara circular para la partícula
            for dy in range(-size, size+1):
                for dx in range(-size, size+1):
                    if dx*dx + dy*dy <= size*size:
                        nx, ny = px + dx, py + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            frame[ny, nx] = [brightness, brightness//2, brightness//3]
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.7)

def create_beat_bars(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea barras de visualización de audio"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Número de barras
        num_bars = 20
        bar_width = w // num_bars
        
        for i in range(num_bars):
            # Altura de cada barra basada en frecuencias simuladas
            frequency = (i + 1) * 100  # Frecuencia simulada
            phase = t * frequency / 50 + i * 0.5
            intensity = abs(math.sin(phase)) * 0.8 + 0.2
            
            bar_height = int(h * 0.3 * intensity)
            
            # Posición de la barra
            x_start = i * bar_width
            x_end = x_start + bar_width - 2
            y_start = h - bar_height
            
            # Color basado en intensidad
            color_intensity = int(255 * intensity)
            color = [color_intensity//3, color_intensity//2, color_intensity]
            
            # Dibujar barra
            frame[y_start:h, x_start:x_end] = color
        
        return frame
    
    return VideoClip(make_frame, duration=duration)

def create_text_simulation(size: Tuple[int, int], duration: float, concept: Dict[str, Any]) -> VideoClip:
    """Simula texto con efectos visuales (sin usar TextClip)"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Simular diferentes secciones de texto con rectángulos de colores
        progress = (t / duration) % 1.0
        
        # Título (primeros 20%)
        if progress < 0.2:
            # Rectángulo para título - efecto typewriter
            title_progress = progress / 0.2
            title_width = int(w * 0.8 * title_progress)
            title_height = 80
            title_y = h // 6
            title_x = (w - title_width) // 2
            
            frame[title_y:title_y+title_height, title_x:title_x+title_width] = [255, 215, 0]  # Dorado
        
        # Hook (20%-40%)
        elif progress < 0.4:
            hook_progress = (progress - 0.2) / 0.2
            pulse = abs(math.sin(t * 8)) * 0.3 + 0.7
            
            hook_width = int(w * 0.7)
            hook_height = int(60 * pulse)
            hook_y = h // 3
            hook_x = (w - hook_width) // 2
            
            brightness = int(255 * pulse)
            frame[hook_y:hook_y+hook_height, hook_x:hook_x+hook_width] = [brightness, brightness//2, 0]
        
        # Development (40%-70%)
        elif progress < 0.7:
            dev_progress = (progress - 0.4) / 0.3
            slide_x = int(w * (dev_progress - 0.5))
            
            dev_width = int(w * 0.6)
            dev_height = 50
            dev_y = h // 2
            final_x = max(0, min(w - dev_width, slide_x + w//4))
            
            frame[dev_y:dev_y+dev_height, final_x:final_x+dev_width] = [0, 255, 255]  # Cian
        
        # Climax (70%-90%)
        elif progress < 0.9:
            climax_progress = (progress - 0.7) / 0.2
            explosion = abs(math.sin(t * 12)) * 0.5 + 0.5
            
            climax_width = int(w * 0.8 * explosion)
            climax_height = int(100 * explosion)
            climax_y = h * 2 // 3
            climax_x = (w - climax_width) // 2
            
            frame[climax_y:climax_y+climax_height, climax_x:climax_x+climax_width] = [255, 0, 255]  # Magenta
        
        # Hashtags (90%-100%)
        else:
            hashtag_progress = (progress - 0.9) / 0.1
            
            for i in range(3):  # 3 hashtags simulados
                tag_width = int(w * 0.25)
                tag_height = 30
                tag_y = h - 200 + i * 50
                tag_x = int(w * 0.1 + (w * 0.8 * hashtag_progress))
                
                if tag_x < w:
                    end_x = min(w, tag_x + tag_width)
                    frame[tag_y:tag_y+tag_height, tag_x:end_x] = [255, 255, 255]  # Blanco
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.8)

def render_wow_reel_simple(concept: Dict[str, Any], audio_path: str, output_path: str) -> str:
    """Renderiza un reel con efectos WOW usando solo efectos procedurales"""
    
    print("🎬 Iniciando renderizado WOW (modo simple)...")
    
    # Cargar audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    print(f"📽️ Duración del audio: {duration:.2f}s")
    
    # Crear capas de efectos
    print("🎨 Creando efectos visuales...")
    
    # 1. Fondo dinámico
    background = create_dynamic_background(DEFAULT_SIZE, duration)
    
    # 2. Overlay geométrico
    geometric = create_geometric_overlay(DEFAULT_SIZE, duration)
    
    # 3. Sistema de partículas
    particles = create_particle_system(DEFAULT_SIZE, duration)
    
    # 4. Barras de visualización
    beat_bars = create_beat_bars(DEFAULT_SIZE, duration)
    
    # 5. Simulación de texto
    text_sim = create_text_simulation(DEFAULT_SIZE, duration, concept)
    
    print("🎭 Componiendo video final...")
    
    # Componer todas las capas
    clips = [background, geometric, particles, beat_bars, text_sim]
    
    final_video = CompositeVideoClip(clips, size=DEFAULT_SIZE)
    final_video = final_video.with_audio(audio_clip).with_duration(duration)
    
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
    
    parser = argparse.ArgumentParser(description="Render TikTok reel con efectos WOW (simple)")
    parser.add_argument("audio", help="Archivo de audio")
    parser.add_argument("concept_json", help="JSON con concepto")
    parser.add_argument("--output", "-o", default="outputs/reel_wow_simple.mp4", help="Archivo de salida")
    
    args = parser.parse_args()
    
    # Cargar concepto
    with open(args.concept_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extraer concepto
    if "tiktok_concepts" in data:
        concept = data["tiktok_concepts"][0]
    else:
        concept = data
    
    # Renderizar
    output = render_wow_reel_simple(concept, args.audio, args.output)
    print(f"🎉 Reel generado exitosamente: {output}")

if __name__ == "__main__":
    main()
