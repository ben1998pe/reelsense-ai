# 🎵 ReelSense AI - Analizador de Música Inteligente

**ReelSense AI** es un sistema avanzado de análisis de música que combina transcripción de audio, análisis de sentimiento y características musicales para proporcionar insights profundos sobre cualquier pieza musical.

## 🚀 Características Principales

- **🎤 Transcripción Inteligente**: Utiliza Whisper AI para transcribir letras de música con alta precisión
- **😊 Análisis de Sentimiento**: Detecta emociones y temas en las letras musicales
- **🔍 Análisis de Audio**: Extrae características como tempo, pitch, energía y brillantez espectral
- **⚡ Preprocesamiento Avanzado**: Filtros de ruido y enfatización de voces para mejor transcripción
- **📊 Post-procesamiento**: Limpieza y validación automática de transcripciones
- **🎯 Múltiples Modelos**: Soporte para modelos Whisper base, small, medium y large

## 📁 Estructura del Proyecto

```
ReelSense AI/
├── 📁 inputs/              # Archivos de audio de entrada
├── 📁 outputs/             # Resultados del análisis
├── 📁 src/                 # Código fuente principal
│   └── music_analyzer_improved.py
├── 📁 tests/               # Scripts de prueba
│   └── test_analyzer.py
├── 📁 docs/                # Documentación
│   └── ejemplos_uso.md
├── 📁 config/              # Configuraciones
│   └── settings.py
├── 📄 main.py              # Script principal
├── 📄 requirements.txt     # Dependencias
└── 📄 README.md           # Este archivo
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- FFmpeg instalado en el sistema

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd "ReelSense AI"
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Instalar FFmpeg (Windows)
1. Descargar desde [gyan.dev](https://gyan.dev/ffmpeg/)
2. Extraer en `C:\ffmpeg\`
3. Agregar `C:\ffmpeg\bin` al PATH del sistema

## 🎯 Uso

### Análisis Básico
```bash
# Usar el script principal
python main.py "inputs/tu_cancion.mp3"

# O directamente desde src/
python src/music_analyzer_improved.py "inputs/tu_cancion.mp3"
```

### Opciones Avanzadas
```bash
# Usar modelo más preciso (más lento)
python src/music_analyzer_improved.py "inputs/tu_cancion.mp3" -m medium

# Guardar resultados en archivo específico
python src/music_analyzer_improved.py "inputs/tu_cancion.mp3" -o "outputs/mi_analisis.json"
```

### Ejecutar Pruebas
```bash
python tests/test_analyzer.py
```

## 📊 Formatos Soportados

- **Audio**: MP3, WAV, FLAC, M4A, OGG
- **Salida**: JSON con análisis completo

## 🔧 Configuración

Edita `config/settings.py` para personalizar:
- Modelo Whisper por defecto
- Frecuencias de filtrado de voces
- Umbrales de sentimiento
- Directorios de entrada/salida

## 📈 Ejemplo de Resultado

```json
{
  "audio_info": {
    "file_path": "inputs/ladygaga.mp3",
    "duration_seconds": 224.35,
    "sample_rate": 44100,
    "average_rms": 0.2656,
    "average_pitch_hz": 1332.5,
    "tempo_bpm": 126.0,
    "spectral_centroid": 2862.2
  },
  "transcription": "Hold me in your arms tonight...",
  "sentiment_analysis": {
    "sentiment": "Positivo",
    "polarity": 0.052,
    "subjectivity": 0.386,
    "confidence": 0.512,
    "emotions": {"amor": 2, "energía": 2, "misterio": 4},
    "themes": {"romance": 1, "naturaleza": 2, "vida": 3}
  }
}
```

## 🧪 Pruebas

El proyecto incluye un conjunto completo de pruebas:
- Análisis de sentimiento
- Características de audio
- Cálculo de confianza de transcripción

## 🚀 Próximas Funcionalidades

- [ ] Análisis de género musical
- [ ] Detección de instrumentos
- [ ] Comparación entre canciones
- [ ] API REST
- [ ] Interfaz web
- [ ] Análisis en tiempo real

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **OpenAI Whisper** por la transcripción de audio
- **TextBlob** por el análisis de sentimiento
- **Librosa** por el procesamiento de audio
- **FFmpeg** por el procesamiento multimedia

## 📞 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la documentación en `docs/`
- Ejecuta las pruebas para verificar la instalación

---

**🎵 ReelSense AI** - Transformando la música en insights inteligentes
