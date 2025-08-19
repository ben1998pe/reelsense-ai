#!/usr/bin/env python3
"""
Analizador de Música Integrado con Generador de TikTok Reels
Combina análisis musical y generación de contenido viral para TikTok
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from music_analyzer_improved import ImprovedMusicAnalyzer
from tiktok_generator import TikTokReelGenerator

class IntegratedMusicAnalyzer:
    def __init__(self, openrouter_api_key: str = None, whisper_model: str = "small"):
        """
        Inicializa el analizador integrado.
        
        Args:
            openrouter_api_key: API key de OpenRouter
            whisper_model: Modelo Whisper a usar
        """
        print("🎵🎬 ANALIZADOR DE MÚSICA INTEGRADO - REELSENSE AI")
        print("=" * 70)
        
        # Inicializar analizador de música
        self.music_analyzer = ImprovedMusicAnalyzer(model_size=whisper_model)
        
        # Inicializar generador de TikTok (opcional)
        self.tiktok_generator = None
        if openrouter_api_key:
            try:
                self.tiktok_generator = TikTokReelGenerator(api_key=openrouter_api_key)
                print("✅ Generador de TikTok inicializado con modelo gratuito")
            except Exception as e:
                print(f"⚠️ Generador de TikTok no disponible: {str(e)}")
        else:
            print("ℹ️ Generador de TikTok no configurado (sin API key)")
    
    def analyze_and_generate_tiktok(self, audio_path: str, generate_concepts: bool = True, 
                                   concept_count: int = 3) -> Dict[str, Any]:
        """
        Analiza música y genera conceptos de TikTok reels.
        
        Args:
            audio_path: Ruta al archivo de audio
            generate_concepts: Si generar conceptos de TikTok
            concept_count: Número de conceptos a generar
            
        Returns:
            Diccionario con análisis musical y conceptos de TikTok
        """
        print(f"\n🎵 Analizando música: {audio_path}")
        print("=" * 50)
        
        # 1. Análisis musical
        music_analysis = self.music_analyzer.analyze_music_segment(audio_path)
        
        if "error" in music_analysis:
            return music_analysis
        
        # 2. Generar conceptos de TikTok si está disponible
        tiktok_concepts = None
        if generate_concepts and self.tiktok_generator:
            print(f"\n🎬 Generando {concept_count} conceptos de TikTok reels...")
            print("=" * 50)
            
            try:
                tiktok_concepts = self.tiktok_generator.generate_multiple_concepts(
                    music_analysis, count=concept_count
                )
                print(f"✅ {len(tiktok_concepts)} conceptos generados exitosamente!")
                
            except Exception as e:
                print(f"❌ Error generando conceptos de TikTok: {str(e)}")
                tiktok_concepts = None
        
        # 3. Combinar resultados
        integrated_result = {
            "music_analysis": music_analysis,
            "tiktok_concepts": tiktok_concepts,
            "analysis_metadata": {
                "integrated_analysis": True,
                "tiktok_generation": tiktok_concepts is not None,
                "concepts_generated": len(tiktok_concepts) if tiktok_concepts else 0
            }
        }
        
        return integrated_result
    
    def save_integrated_results(self, results: Dict[str, Any], output_path: str = None) -> str:
        """
        Guarda los resultados integrados en un archivo JSON.
        
        Args:
            results: Resultados del análisis integrado
            output_path: Ruta del archivo de salida
            
        Returns:
            Ruta del archivo guardado
        """
        if not output_path:
            timestamp = results['music_analysis']['audio_info']['file_path'].split('/')[-1].split('.')[0]
            output_path = f"outputs/integrated_analysis_{timestamp}.json"
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Guardar resultados
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Resultados integrados guardados en: {output_path}")
        return output_path
    
    def display_integrated_results(self, results: Dict[str, Any]):
        """
        Muestra los resultados integrados de manera organizada.
        
        Args:
            results: Resultados del análisis integrado
        """
        print("\n" + "=" * 70)
        print("🎵🎬 RESULTADOS DEL ANÁLISIS INTEGRADO")
        print("=" * 70)
        
        # Mostrar análisis musical
        music_analysis = results['music_analysis']
        audio_info = music_analysis['audio_info']
        sentiment = music_analysis['sentiment_analysis']
        
        print(f"📁 Archivo: {audio_info['file_path']}")
        print(f"⏱️  Duración: {audio_info['duration_seconds']} segundos")
        print(f"🥁 Tempo: {audio_info['tempo_bpm']} BPM")
        print(f"🎼 Pitch: {audio_info['average_pitch_hz']} Hz")
        print(f"✨ Brillo: {audio_info['spectral_centroid']}")
        
        print(f"\n📝 TRANSCRIPCIÓN:")
        print(f"'{music_analysis['transcription'][:100]}...'")
        
        print(f"\n😊 SENTIMIENTO: {sentiment['sentiment']}")
        print(f"   Polaridad: {sentiment['polarity']:.3f}")
        print(f"   Confianza: {sentiment['confidence']:.1%}")
        
        if sentiment['emotions']:
            print(f"   Emociones: {', '.join([f'{k}: {v}' for k, v in sentiment['emotions'].items()])}")
        
        # Mostrar conceptos de TikTok
        tiktok_concepts = results.get('tiktok_concepts')
        if tiktok_concepts:
            print(f"\n🎬 CONCEPTOS DE TIKTOK REELS GENERADOS:")
            print("=" * 50)
            
            for i, concept in enumerate(tiktok_concepts, 1):
                print(f"\n📱 CONCEPTO {i}: {concept['concept_title']}")
                print(f"   🎯 Gancho: {concept['viral_hook']}")
                print(f"   👥 Audiencia: {concept['target_audience']}")
                print(f"   🏷️ Hashtags: {', '.join(concept['hashtags'][:3])}...")
                print(f"   ⚡ Potencial: {concept['viral_potential'][:50]}...")
        
        # Metadatos
        metadata = results['analysis_metadata']
        print(f"\n🔧 METADATOS:")
        print(f"   Análisis integrado: {'✅ Sí' if metadata['integrated_analysis'] else '❌ No'}")
        print(f"   Generación TikTok: {'✅ Sí' if metadata['tiktok_generation'] else '❌ No'}")
        print(f"   Conceptos generados: {metadata['concepts_generated']}")

def main():
    """Función principal del script integrado."""
    parser = argparse.ArgumentParser(
        description="Analizador de música integrado con generador de TikTok reels"
    )
    parser.add_argument("audio_path", help="Ruta al archivo de audio")
    parser.add_argument("--output", "-o", help="Archivo de salida para guardar resultados")
    parser.add_argument("--model", "-m", choices=["base", "small", "medium", "large"], 
                       default="small", help="Tamaño del modelo Whisper")
    parser.add_argument("--no-tiktok", action="store_true", 
                       help="No generar conceptos de TikTok")
    parser.add_argument("--concepts", "-c", type=int, default=3,
                       help="Número de conceptos de TikTok a generar")
    parser.add_argument("--api-key", help="API key de OpenRouter (opcional)")
    
    args = parser.parse_args()
    
    # Obtener API key
    api_key = args.api_key or os.getenv('OPENROUTER_API_KEY')
    
    # Crear analizador integrado
    analyzer = IntegratedMusicAnalyzer(
        openrouter_api_key=api_key,
        whisper_model=args.model
    )
    
    # Analizar y generar
    results = analyzer.analyze_and_generate_tiktok(
        audio_path=args.audio_path,
        generate_concepts=not args.no_tiktok,
        concept_count=args.concepts
    )
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Mostrar resultados
    analyzer.display_integrated_results(results)
    
    # Guardar resultados
    if args.output:
        analyzer.save_integrated_results(results, args.output)
    else:
        analyzer.save_integrated_results(results)
    
    print("\n" + "=" * 70)
    print("🎵🎬 ¡ANÁLISIS INTEGRADO COMPLETADO!")
    print("=" * 70)

if __name__ == "__main__":
    main()
