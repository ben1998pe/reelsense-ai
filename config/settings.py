"""
Configuración por defecto para ReelSense AI
"""

# Configuración del modelo Whisper
WHISPER_MODEL = "small"  # Opciones: "base", "small", "medium", "large"

# Configuración de audio
AUDIO_SAMPLE_RATE = 44100  # Hz
AUDIO_CHUNK_SIZE = 1024

# Configuración de preprocesamiento
VOCAL_FREQ_LOW = 300   # Hz - Frecuencia baja para voces
VOCAL_FREQ_HIGH = 3400 # Hz - Frecuencia alta para voces
NOISE_REDUCTION_STRENGTH = 0.1  # Fuerza del filtro de ruido

# Configuración de análisis de sentimiento
SENTIMENT_THRESHOLDS = {
    "very_positive": 0.2,
    "positive": 0.05,
    "negative": -0.05,
    "very_negative": -0.2
}

# Configuración de salida
DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_OUTPUT_FORMAT = "json"

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
