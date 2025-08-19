#!/usr/bin/env python3
"""
TikTok Reel Generator - Genera contenido creativo para TikTok basado en análisis musical
"""

import openai
import json
import os
from typing import Dict, Any, List
from datetime import datetime

class TikTokReelGenerator:
    def __init__(self, api_key: str = None, model: str = "openai/gpt-oss-20b:free"):
        """
        Inicializa el generador de reels de TikTok.
        
        Args:
            api_key: API key de OpenRouter (opcional, busca en variables de entorno)
            model: Modelo de IA a usar
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "API key no encontrada. Establece OPENROUTER_API_KEY en variables de entorno "
                "o pásala como parámetro."
            )
        
        # Configurar cliente OpenAI para OpenRouter
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        print(f"🎬 Generador de TikTok Reels inicializado con modelo: {model}")
    
    def generate_reel_concept(self, music_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera un concepto completo para un reel de TikTok basado en análisis musical.
        
        Args:
            music_analysis: Resultado del análisis musical
            
        Returns:
            Diccionario con el concepto del reel
        """
        print("🎬 Generando concepto de reel para TikTok...")
        
        # Extraer información clave del análisis
        transcription = music_analysis.get('transcription', '')
        sentiment = music_analysis.get('sentiment_analysis', {})
        audio_info = music_analysis.get('audio_info', {})
        
        # Crear prompt inteligente
        prompt = self._create_tiktok_prompt(transcription, sentiment, audio_info)
        
        try:
            # Llamar a OpenRouter
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto creador de contenido viral para TikTok. 
                        Tu trabajo es analizar música y crear conceptos de reels que sean:
                        - Altamente virales y engaging
                        - Creativos e innovadores
                        - Perfectamente sincronizados con la música
                        - Adaptados al algoritmo de TikTok
                        
                        IMPORTANTE: Responde ÚNICAMENTE en formato JSON válido, sin texto adicional.
                        El JSON debe empezar con { y terminar con }."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # Creatividad moderada para mejor consistencia
                max_tokens=1500
            )
            
            # Extraer respuesta
            content = response.choices[0].message.content.strip()
            
            # Limpiar la respuesta para extraer solo el JSON
            content = self._extract_json_from_response(content)
            
            # Si no se pudo extraer JSON, usar fallback
            if not content:
                print("⚠️ Usando concepto de respaldo...")
                return self._generate_fallback_concept(music_analysis)
            
            # Parsear JSON
            reel_concept = json.loads(content)
            
            # Agregar metadatos
            reel_concept['generated_at'] = datetime.now().isoformat()
            reel_concept['model_used'] = self.model
            reel_concept['music_analysis_summary'] = {
                'duration': audio_info.get('duration_seconds', 0),
                'tempo': audio_info.get('tempo_bpm', 0),
                'sentiment': sentiment.get('sentiment', 'Unknown'),
                'emotions': sentiment.get('emotions', {})
            }
            
            print("✅ Concepto de reel generado exitosamente!")
            return reel_concept
            
        except Exception as e:
            print(f"❌ Error generando concepto: {str(e)}")
            return self._generate_fallback_concept(music_analysis)
    
    def _create_tiktok_prompt(self, transcription: str, sentiment: Dict, audio_info: Dict) -> str:
        """
        Crea un prompt inteligente para OpenRouter basado en el análisis musical.
        """
        emotions = sentiment.get('emotions', {})
        themes = sentiment.get('themes', {})
        tempo = audio_info.get('tempo_bpm', 0)
        duration = audio_info.get('duration_seconds', 0)
        
        prompt = f"""
        Analiza esta música y crea un concepto viral para TikTok:

        🎵 LETRA TRANSCRITA:
        "{transcription[:200]}..."

        😊 SENTIMIENTO: {sentiment.get('sentiment', 'Unknown')}
        🎭 EMOCIONES: {', '.join([f'{k}: {v}' for k, v in emotions.items()])}
        🎨 TEMAS: {', '.join([f'{k}: {v}' for k, v in themes.items()])}
        🥁 TEMPO: {tempo} BPM
        ⏱️ DURACIÓN: {duration} segundos

        📱 GENERA UN CONCEPTO DE REEL EN ESTE FORMATO JSON:
        {{
            "concept_title": "Título creativo del concepto",
            "viral_hook": "Gancho viral en 3-5 segundos",
            "story_structure": {{
                "intro": "Qué mostrar en 0-3 segundos",
                "hook_moment": "Momento de gancho en 3-6 segundos",
                "development": "Desarrollo del contenido en 6-15 segundos",
                "climax": "Momento más impactante en 15-20 segundos",
                "closing": "Cierre y call-to-action en 20-30 segundos"
            }},
            "visual_elements": [
                "Elemento visual 1",
                "Elemento visual 2",
                "Elemento visual 3"
            ],
            "transitions": [
                "Transición 1 (timing específico)",
                "Transición 2 (timing específico)",
                "Transición 3 (timing específico)"
            ],
            "effects": [
                "Efecto 1 (cuándo aplicarlo)",
                "Efecto 2 (cuándo aplicarlo)"
            ],
            "hashtags": [
                "hashtag1",
                "hashtag2",
                "hashtag3",
                "hashtag4",
                "hashtag5"
            ],
            "target_audience": "Audiencia objetivo específica",
            "viral_potential": "Por qué será viral",
            "music_sync_tips": [
                "Consejo 1 para sincronizar con la música",
                "Consejo 2 para sincronizar con la música"
            ]
        }}

        IMPORTANTE: 
        - El reel debe ser de máximo 30 segundos
        - Debe ser súper viral y engaging
        - Debe sincronizarse perfectamente con el beat
        - Usa la letra y emociones de la música
        - Sé creativo e innovador
        """
        
        return prompt
    
    def _extract_json_from_response(self, content: str) -> str:
        """
        Extrae el JSON válido de la respuesta del modelo.
        
        Args:
            content: Respuesta completa del modelo
            
        Returns:
            String con solo el JSON válido
        """
        # Buscar el primer { y último }
        start = content.find('{')
        end = content.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            json_content = content[start:end+1]
            
            # Verificar que sea JSON válido
            try:
                json.loads(json_content)
                return json_content
            except json.JSONDecodeError:
                pass
        
        # Si no se puede extraer JSON válido, generar uno básico
        print("⚠️ No se pudo extraer JSON válido de la respuesta del modelo")
        return ""
    
    def _generate_fallback_concept(self, music_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera un concepto básico si falla la IA.
        """
        print("⚠️ Generando concepto básico como respaldo...")
        
        sentiment = music_analysis.get('sentiment_analysis', {})
        emotions = sentiment.get('emotions', {})
        
        return {
            "concept_title": "Reel Musical Automático",
            "viral_hook": "¡Descubre el poder de esta música!",
            "story_structure": {
                "intro": "Mostrar título de la canción (0-3s)",
                "hook_moment": "Pregunta retórica sobre la música (3-6s)",
                "development": "Mostrar letra clave de la canción (6-15s)",
                "climax": "Efecto visual impactante (15-20s)",
                "closing": "Call-to-action para seguir (20-30s)"
            },
            "visual_elements": [
                "Texto animado de la letra",
                "Efectos de partículas",
                "Transiciones suaves"
            ],
            "transitions": [
                "Fade in al inicio",
                "Slide transition en el medio",
                "Zoom out al final"
            ],
            "effects": [
                "Glitch effect en momentos clave",
                "Color grading según el sentimiento"
            ],
            "hashtags": [
                "music",
                "viral",
                "trending",
                "fyp",
                "musicanalysis"
            ],
            "target_audience": "Amantes de la música y TikTok",
            "viral_potential": "Contenido musical auténtico y engaging",
            "music_sync_tips": [
                "Sincronizar transiciones con el beat",
                "Usar efectos en momentos de alta energía"
            ],
            "generated_at": datetime.now().isoformat(),
            "model_used": "fallback",
            "music_analysis_summary": {
                "duration": music_analysis.get('audio_info', {}).get('duration_seconds', 0),
                "tempo": music_analysis.get('audio_info', {}).get('tempo_bpm', 0),
                "sentiment": sentiment.get('sentiment', 'Unknown'),
                "emotions": emotions
            }
        }
    
    def generate_multiple_concepts(self, music_analysis: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
        """
        Genera múltiples conceptos de reels para dar opciones.
        
        Args:
            music_analysis: Resultado del análisis musical
            count: Número de conceptos a generar
            
        Returns:
            Lista de conceptos de reels
        """
        print(f"🎬 Generando {count} conceptos diferentes de reels...")
        
        concepts = []
        for i in range(count):
            print(f"   Generando concepto {i+1}/{count}...")
            
            # Modificar ligeramente el prompt para variación
            concept = self.generate_reel_concept(music_analysis)
            concept['concept_number'] = i + 1
            concept['variation_style'] = f"Estilo {i+1}"
            
            concepts.append(concept)
        
        return concepts
    
    def save_concepts(self, concepts: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        Guarda los conceptos generados en un archivo JSON.
        
        Args:
            concepts: Lista de conceptos de reels
            output_path: Ruta del archivo de salida
            
        Returns:
            Ruta del archivo guardado
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"outputs/tiktok_concepts_{timestamp}.json"
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Guardar conceptos
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(concepts, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Conceptos guardados en: {output_path}")
        return output_path

def main():
    """Función principal para probar el generador."""
    print("🎬 TIKTOK REEL GENERATOR - REELSENSE AI")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY no encontrada en variables de entorno")
        print("💡 Para configurarla:")
        print("   Windows: set OPENROUTER_API_KEY=tu_api_key")
        print("   Linux/Mac: export OPENROUTER_API_KEY=tu_api_key")
        return
    
    # Crear generador
    generator = TikTokReelGenerator(api_key=api_key)
    
    # Ejemplo de análisis musical (simulado)
    sample_analysis = {
        "transcription": "Hold me in your arms tonight in the magic of the dark moonlight",
        "sentiment_analysis": {
            "sentiment": "Positivo",
            "emotions": {"amor": 2, "misterio": 3, "energía": 1},
            "themes": {"romance": 2, "naturaleza": 1}
        },
        "audio_info": {
            "duration_seconds": 30,
            "tempo_bpm": 126
        }
    }
    
    # Generar concepto
    concept = generator.generate_reel_concept(sample_analysis)
    
    # Mostrar resultado
    print("\n🎬 CONCEPTO GENERADO:")
    print(f"Título: {concept['concept_title']}")
    print(f"Gancho: {concept['viral_hook']}")
    print(f"Hashtags: {', '.join(concept['hashtags'])}")
    
    # Guardar resultado
    generator.save_concepts([concept])

if __name__ == "__main__":
    main()
