# 🎬 Integración con TikTok Reels - ReelSense AI

## 🚀 **¿Qué hace esta funcionalidad?**

**ReelSense AI** ahora puede **analizar música Y generar conceptos virales para TikTok reels automáticamente** usando **OpenRouter AI**.

## 🔥 **Flujo Completo:**

```
🎵 Música → 🧠 Análisis Musical → 🤖 OpenRouter AI → 🎬 Concepto TikTok Viral
```

### **1. 🎵 Análisis Musical:**
- Transcripción de letra con Whisper AI
- Análisis de sentimiento y emociones
- Características de audio (tempo, pitch, energía)
- Temas musicales detectados

### **2. 🤖 OpenRouter AI:**
- Recibe el análisis musical completo
- Genera **conceptos creativos** para TikTok
- **Guiones del reel** basados en la música
- **Hashtags estratégicos** para viralizar
- **Timing perfecto** con el beat

### **3. 🎬 Concepto TikTok:**
- **Storytelling** basado en la letra
- **Transiciones** sincronizadas
- **Efectos visuales** que coinciden con emociones
- **Call-to-action** viral

## 🛠️ **Instalación y Configuración:**

### **1. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### **2. Configurar OpenRouter API:**
```bash
python config/setup_openrouter.py
```

**O manualmente:**
```bash
# Windows (PowerShell)
set OPENROUTER_API_KEY=tu_api_key_aqui

# Linux/Mac
export OPENROUTER_API_KEY=tu_api_key_aqui
```

### **3. Obtener API Key gratuita:**
1. Ve a [https://openrouter.ai/](https://openrouter.ai/)
2. Crea cuenta gratuita
3. Ve a "API Keys"
4. Crea nueva API key
5. **$5 de crédito mensual gratis** 🆓

## 🎯 **Uso:**

### **Análisis Básico (sin TikTok):**
```bash
python src/music_analyzer_improved.py "inputs/tu_cancion.mp3"
```

### **Análisis + TikTok Reels:**
```bash
python src/music_analyzer_with_tiktok.py "inputs/tu_cancion.mp3"
```

### **Generar múltiples conceptos:**
```bash
python src/music_analyzer_with_tiktok.py "inputs/tu_cancion.mp3" --concepts 5
```

### **Usar modelo Whisper específico:**
```bash
python src/music_analyzer_with_tiktok.py "inputs/tu_cancion.mp3" -m medium
```

### **Guardar en archivo específico:**
```bash
python src/music_analyzer_with_tiktok.py "inputs/tu_cancion.mp3" -o "mi_analisis.json"
```

## 📊 **Ejemplo de Resultado:**

```json
{
  "music_analysis": {
    "transcription": "Hold me in your arms tonight...",
    "sentiment_analysis": {
      "sentiment": "Positivo",
      "emotions": {"amor": 2, "misterio": 4}
    },
    "audio_info": {
      "tempo_bpm": 126,
      "duration_seconds": 30
    }
  },
  "tiktok_concepts": [
    {
      "concept_title": "El Poder Transformador del Amor en la Oscuridad",
      "viral_hook": "¿Alguna vez te has sentido perdido en la oscuridad?",
      "story_structure": {
        "intro": "Silueta en la luna (0-3s)",
        "hook_moment": "Pregunta retórica (3-6s)",
        "development": "Letra clave (6-15s)",
        "climax": "Efectos de fuego (15-20s)",
        "closing": "Call-to-action (20-30s)"
      },
      "hashtags": ["#LadyGaga", "#TikTokMusic", "#ViralReel", "#LoveStory"],
      "target_audience": "Amantes de música romántica y misteriosa",
      "viral_potential": "Contenido emocional que conecta con sentimientos universales"
    }
  ]
}
```

## 🎨 **Tipos de Conceptos Generados:**

### **1. 🎭 Reels Emocionales:**
- Basados en sentimientos de la música
- Storytelling personal
- Conexión emocional con la audiencia

### **2. 🎵 Reels Musicales:**
- Sincronización perfecta con el beat
- Efectos visuales rítmicos
- Transiciones musicales

### **3. 🎬 Reels Narrativos:**
- Historias basadas en la letra
- Desarrollo de personajes
- Arcos narrativos completos

### **4. 🚀 Reels Virales:**
- Ganchos impactantes
- Hashtags trending
- Call-to-action efectivos

## 🔧 **Configuración Avanzada:**

### **Modelos de IA disponibles:**
- **GPT-4**: Máxima creatividad y calidad
- **Claude**: Excelente para storytelling
- **GPT-3.5**: Rápido y eficiente
- **Llama**: Open source y personalizable

### **Personalizar prompts:**
Edita `src/tiktok_generator.py` para modificar:
- Estilo de contenido
- Longitud de reels
- Tipos de conceptos
- Hashtags preferidos

## 💰 **Costos:**

### **Plan Gratuito:**
- **$5 de crédito mensual** 🆓
- **Suficiente para 50-100 análisis** mensuales
- **Sin tarjeta de crédito** requerida

### **Plan Pago:**
- **Pay-as-you-go** (solo pagas lo que uses)
- **Sin límites** mensuales
- **Modelos más avanzados**

## 🚀 **Próximas Funcionalidades:**

- [ ] **Generación de storyboards visuales**
- [ ] **Sugerencias de música trending**
- [ ] **Análisis de competencia**
- [ ] **Métricas de viralización**
- [ ] **Integración con TikTok API**

## 🤝 **Soporte:**

### **Problemas comunes:**
1. **API key no válida**: Verifica en [OpenRouter Dashboard](https://openrouter.ai/keys)
2. **Sin créditos**: Espera al siguiente mes o actualiza tu plan
3. **Error de conexión**: Verifica tu conexión a internet

### **Obtener ayuda:**
- Abre un issue en GitHub
- Revisa la documentación
- Ejecuta `python config/setup_openrouter.py`

## 💡 **Tips para Mejores Resultados:**

1. **Usa música de alta calidad** para mejor transcripción
2. **Canciones de 15-60 segundos** para reels óptimos
3. **Música con letras claras** para mejor análisis
4. **Experimenta con diferentes modelos** de IA
5. **Personaliza los prompts** según tu estilo

---

**🎵🎬 ReelSense AI** - Transformando música en contenido viral para TikTok
