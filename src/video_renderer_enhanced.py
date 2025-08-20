#!/usr/bin/env python3
"""
Video Renderer Enhanced - Genera reels TikTok con efectos WOW mejorados
"""

import os
import json
import math
import random
from typing import Dict, Any, Tuple, List
import numpy as np

# MoviePy imports
try:
    from moviepy.editor import VideoClip, CompositeVideoClip, ColorClip, AudioFileClip, ImageClip
except ImportError:
    from moviepy.video.VideoClip import VideoClip, ColorClip, ImageClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip

# PIL para texto personalizado
from PIL import Image, ImageDraw, ImageFont

DEFAULT_SIZE = (1080, 1920)  # 9:16 vertical
DEFAULT_FPS = 30

def create_epic_background(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea un fondo épico con ondas de energía y colores dramáticos"""
    w, h = size
    
    def make_frame(t):
        # Crear patrones de energía más dramáticos
        x = np.linspace(0, 8*np.pi, w)
        y = np.linspace(0, 12*np.pi, h)
        X, Y = np.meshgrid(x, y)
        
        # Ondas de energía que pulsan
        energy_wave = np.sin(X + t * 3) * np.cos(Y + t * 2.5)
        energy_wave += np.cos(X * 3 + t * 4) * np.sin(Y * 2 + t * 3)
        
        # Efecto de vórtice en el centro
        center_x, center_y = w//2, h//2
        dist = np.sqrt((np.arange(w) - center_x)**2 + (np.arange(h)[:, None] - center_y)**2)
        vortex = np.sin(dist/50 + t*6) * np.exp(-dist/200)
        
        # Combinar efectos
        combined = (energy_wave + vortex) / 2
        
        # Colores más dramáticos y contrastantes
        # Rojo intenso para energía
        r = np.clip((combined + 1) * 150 + 50, 0, 255)
        # Verde eléctrico
        g = np.clip((np.sin(combined * 2*np.pi + t*2) + 1) * 180 + 20, 0, 255)
        # Azul profundo
        b = np.clip((np.cos(combined * np.pi + t*3) + 1) * 120 + 80, 0, 255)
        
        # Añadir destellos aleatorios
        if random.random() < 0.1:  # 10% de probabilidad por frame
            flash_mask = np.random.random((h, w)) < 0.01
            r[flash_mask] = 255
            g[flash_mask] = 255
            b[flash_mask] = 255
        
        frame = np.stack([r, g, b], axis=2).astype(np.uint8)
        return frame
    
    return VideoClip(make_frame, duration=duration)

def create_beat_sync_effects(size: Tuple[int, int], duration: float, audio_path: str) -> VideoClip:
    """Crea efectos sincronizados con el beat de la música"""
    w, h = size
    
    # Simular análisis de beat (en una implementación real usaríamos librosa)
    beat_times = np.linspace(0, duration, int(duration * 2))  # 2 beats por segundo
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Encontrar el beat más cercano
        closest_beat = min(beat_times, key=lambda x: abs(x - t))
        beat_intensity = 1.0 / (1.0 + abs(t - closest_beat) * 10)
        
        # Círculos de beat que pulsan
        center_x, center_y = w//2, h//2
        
        # Círculo principal de beat
        beat_radius = int(300 * beat_intensity)
        y_indices, x_indices = np.ogrid[:h, :w]
        beat_mask = (x_indices - center_x)**2 + (y_indices - center_y)**2 <= beat_radius**2
        
        # Color del beat (rojo intenso)
        beat_color = int(255 * beat_intensity)
        frame[beat_mask] = [beat_color, max(0, beat_color//4), 0]
        
        # Ondas de beat que se expanden
        for i in range(3):
            wave_radius = int(400 + i*200 + 200*beat_intensity)
            wave_mask = (x_indices - center_x)**2 + (y_indices - center_y)**2 <= wave_radius**2
            wave_mask &= (x_indices - center_x)**2 + (y_indices - center_y)**2 > (wave_radius-50)**2
            
            wave_intensity = beat_intensity * (1 - i*0.3)
            wave_color = int(255 * wave_intensity)
            frame[wave_mask] = [wave_color//2, wave_color, wave_color//2]
        
        # Líneas de energía que se mueven al ritmo
        for i in range(5):
            line_y = int(h/2 + 300 * math.sin(t * 4 + i * math.pi/3))
            if 0 <= line_y < h:
                line_width = int(20 * beat_intensity)
                start_y = max(0, line_y - line_width//2)
                end_y = min(h, line_y + line_width//2)
                frame[start_y:end_y, :] = [255, 255, 0]  # Línea amarilla brillante
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.8)

def create_particle_explosion(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea sistema de partículas explosivas"""
    w, h = size
    
    # Generar partículas
    num_particles = 200
    particles = []
    
    for _ in range(num_particles):
        particle = {
            'x': random.uniform(0, w),
            'y': random.uniform(0, h),
            'vx': random.uniform(-200, 200),
            'vy': random.uniform(-200, 200),
            'life': random.uniform(0.5, 2.0),
            'color': [random.randint(200, 255), random.randint(100, 255), random.randint(0, 255)]
        }
        particles.append(particle)
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Actualizar y dibujar partículas
        for particle in particles:
            # Actualizar posición
            particle['x'] += particle['vx'] * 0.016  # 60 FPS
            particle['y'] += particle['vy'] * 0.016
            
            # Gravedad
            particle['vy'] += 50 * 0.016
            
            # Vida
            particle['life'] -= 0.016
            
            # Dibujar si está vivo y en pantalla
            if (particle['life'] > 0 and 
                0 <= particle['x'] < w and 0 <= particle['y'] < h):
                
                # Tamaño basado en la vida
                size = int(10 * particle['life'])
                x, y = int(particle['x']), int(particle['y'])
                
                # Dibujar partícula
                for dy in range(-size, size+1):
                    for dx in range(-size, size+1):
                        px, py = x + dx, y + dy
                        if (0 <= px < w and 0 <= py < h and 
                            dx*dx + dy*dy <= size*size):
                            # Color con transparencia basada en la vida
                            alpha = particle['life']
                            frame[py, px] = [np.clip(int(c * alpha), 0, 255) for c in particle['color']]
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.9)

def create_text_effects(size: Tuple[int, int], duration: float, concept: Dict[str, Any]) -> VideoClip:
    """Crea efectos de texto dramáticos y animados"""
    w, h = size
    
    # Extraer información del concepto
    title = concept.get('concept_title', 'TikTok Reel')
    hook = concept.get('viral_hook', '¡Mira esto!')
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Título principal (0-30%)
        if t < duration * 0.3:
            title_progress = t / (duration * 0.3)
            
            # Efecto de aparición con glitch
            if title_progress < 0.8:
                # Texto que aparece letra por letra
                chars_to_show = int(len(title) * title_progress)
                display_text = title[:chars_to_show]
                
                # Simular texto (rectángulos blancos)
                char_width = w // len(title)
                for i, char in enumerate(display_text):
                    if i < chars_to_show:
                        x = w//2 - (len(title) * char_width)//2 + i * char_width
                        y = h//4
                        
                        # Efecto de glitch aleatorio
                        if random.random() < 0.1:
                            y += random.randint(-5, 5)
                        
                        # Dibujar "letra"
                        frame[y:y+80, x:x+char_width-10] = [255, 255, 255]
                        
                        # Borde de color
                        frame[y:y+80, x:x+char_width-10] = [255, 0, 0]
            
            # Efecto de explosión al final
            else:
                explosion_progress = (title_progress - 0.8) / 0.2
                explosion_radius = int(400 * explosion_progress)
                
                center_x, center_y = w//2, h//4 + 40
                y_indices, x_indices = np.ogrid[:h, :w]
                explosion_mask = (x_indices - center_x)**2 + (y_indices - center_y)**2 <= explosion_radius**2
                
                explosion_color = int(255 * (1 - explosion_progress))
                frame[explosion_mask] = [explosion_color, explosion_color//2, 0]
        
        # Hook viral (30%-60%)
        elif t < duration * 0.6:
            hook_progress = (t - duration * 0.3) / (duration * 0.3)
            
            # Efecto de máquina de escribir
            chars_to_show = int(len(hook) * hook_progress)
            display_text = hook[:chars_to_show]
            
            # Simular texto con efecto de cursor parpadeante
            char_width = w // len(hook)
            for i, char in enumerate(display_text):
                x = w//2 - (len(hook) * char_width)//2 + i * char_width
                y = h//2
                
                # Color del texto
                text_color = [0, 255, 255]  # Cian
                
                # Cursor parpadeante
                if i == chars_to_show - 1 and random.random() < 0.5:
                    text_color = [255, 255, 255]  # Blanco para el cursor
                
                frame[y:y+60, x:x+char_width-10] = text_color
        
        # Hashtags (60%-100%)
        else:
            hashtag_progress = (t - duration * 0.6) / (duration * 0.4)
            
            hashtags = ["#Viral", "#Trending", "#MustWatch", "#Amazing"]
            
            for i, hashtag in enumerate(hashtags):
                tag_progress = min(1.0, hashtag_progress * 4 - i)
                if tag_progress > 0:
                    # Efecto de deslizamiento desde la derecha
                    slide_x = int(w * (1 - tag_progress))
                    tag_width = w // 4
                    tag_y = h - 300 + i * 80
                    
                    # Dibujar hashtag
                    if slide_x < w:
                        end_x = min(w, slide_x + tag_width)
                        frame[tag_y:tag_y+50, slide_x:end_x] = [255, 255, 0]  # Amarillo
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.9)

def create_geometric_energy(size: Tuple[int, int], duration: float) -> VideoClip:
    """Crea formas geométricas energéticas"""
    w, h = size
    
    def make_frame(t):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Triángulos que rotan
        center_x, center_y = w//2, h//2
        
        for i in range(6):
            angle = t * 2 + i * math.pi / 3
            size_triangle = 150 + 50 * math.sin(t * 3 + i)
            
            # Puntos del triángulo
            points = []
            for j in range(3):
                point_angle = angle + j * 2 * math.pi / 3
                px = center_x + size_triangle * math.cos(point_angle)
                py = center_y + size_triangle * math.sin(point_angle)
                points.append((int(px), int(py)))
            
            # Dibujar triángulo (aproximación)
            if len(points) == 3:
                # Rellenar triángulo
                for y in range(max(0, min(points[0][1], points[1][1], points[2][1])),
                              min(h, max(points[0][1], points[1][1], points[2][1]))):
                    for x in range(max(0, min(points[0][0], points[1][0], points[2][0])),
                                  min(w, max(points[0][0], points[1][0], points[2][0]))):
                        # Verificar si el punto está dentro del triángulo
                        if (x - center_x)**2 + (y - center_y)**2 <= size_triangle**2:
                            # Color basado en el tiempo y posición
                            color_r = int(127 * (math.sin(t * 2 + i) + 1))
                            color_g = int(127 * (math.cos(t * 3 + i) + 1))
                            color_b = int(127 * (math.sin(t * 4 + i) + 1))
                            frame[y, x] = [color_r, color_g, color_b]
        
        return frame
    
    return VideoClip(make_frame, duration=duration).with_opacity(0.7)

def render_epic_reel(concept: Dict[str, Any], audio_path: str, output_path: str) -> str:
    """Renderiza un reel épico con efectos WOW mejorados"""
    
    print("🚀 Iniciando renderizado ÉPICO...")
    
    # Cargar audio
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    print(f"📽️ Duración del audio: {duration:.2f}s")
    
    # Crear capas de efectos mejorados
    print("🎨 Creando efectos visuales épicos...")
    
    # 1. Fondo épico
    background = create_epic_background(DEFAULT_SIZE, duration)
    
    # 2. Efectos sincronizados con beat
    beat_effects = create_beat_sync_effects(DEFAULT_SIZE, duration, audio_path)
    
    # 3. Sistema de partículas explosivas
    particles = create_particle_explosion(DEFAULT_SIZE, duration)
    
    # 4. Efectos de texto dramáticos
    text_effects = create_text_effects(DEFAULT_SIZE, duration, concept)
    
    # 5. Formas geométricas energéticas
    geometric = create_geometric_energy(DEFAULT_SIZE, duration)
    
    print("🎭 Componiendo video épico...")
    
    # Componer todas las capas
    clips = [background, beat_effects, particles, text_effects, geometric]
    
    final_video = CompositeVideoClip(clips, size=DEFAULT_SIZE)
    final_video = final_video.with_audio(audio_clip).with_duration(duration)
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("🔄 Renderizando video épico...")
    
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
    
    print(f"✅ Reel ÉPICO completado: {output_path}")
    return output_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Render TikTok reel ÉPICO con efectos WOW mejorados")
    parser.add_argument("audio", help="Archivo de audio")
    parser.add_argument("concept_json", help="JSON con concepto")
    parser.add_argument("--output", "-o", default="outputs/reel_epic.mp4", help="Archivo de salida")
    
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
    output = render_epic_reel(concept, args.audio, args.output)
    print(f"🎉 Reel ÉPICO generado exitosamente: {output}")

if __name__ == "__main__":
    main()
