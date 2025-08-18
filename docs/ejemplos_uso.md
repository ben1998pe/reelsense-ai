# Ejemplos de Uso - ReelSense AI

## 📁 **Diferentes formas de especificar archivos de audio:**

### **1. Archivo en la raíz del proyecto:**
```bash
python music_analyzer.py "cancion.mp3"
```

### **2. Archivo en carpeta específica:**
```bash
python music_analyzer.py "audio_samples/mi_cancion.mp3"
python music_analyzer.py "audio_samples/rock/cancion_rock.mp3"
```

### **3. Ruta relativa desde el proyecto:**
```bash
python music_analyzer.py "../musica/cancion.mp3"
python music_analyzer.py "./audio_samples/cancion.mp3"
```

### **4. Ruta absoluta del sistema:**
```bash
# Windows
python music_analyzer.py "C:\Users\USER\Music\cancion.mp3"
python music_analyzer.py "C:/Users/USER/Desktop/musica/cancion.mp3"

# Linux/Mac
python music_analyzer.py "/home/usuario/musica/cancion.mp3"
```

## 🎵 **Estructura recomendada del proyecto:**
```
ReelSense AI/
├── music_analyzer.py
├── requirements.txt
├── README.md
├── audio_samples/          # ← Carpeta para archivos de prueba
│   ├── cancion1.mp3
│   ├── cancion2.wav
│   └── generos/
│       ├── rock.mp3
│       ├── pop.mp3
│       └── jazz.mp3
└── resultados/             # ← Carpeta para guardar análisis
    ├── analisis1.json
    └── analisis2.json
```

## 💡 **Consejos prácticos:**

### **Para archivos de prueba:**
- Usa la carpeta `audio_samples/` que acabamos de crear
- Mantén archivos cortos (30 segundos - 2 minutos)
- Usa diferentes formatos para probar compatibilidad

### **Para archivos reales:**
- Puedes apuntar a tu carpeta de música personal
- El script funciona con cualquier ruta válida
- Usa comillas si la ruta tiene espacios

### **Ejemplos con la nueva estructura:**
```bash
# Analizar archivo en audio_samples
python music_analyzer.py "audio_samples/mi_cancion.mp3"

# Analizar y guardar en resultados
python music_analyzer.py "audio_samples/cancion.mp3" -o "resultados/analisis.json"

# Analizar archivo en tu carpeta de música
python music_analyzer.py "C:\Users\USER\Music\favoritas\cancion.mp3"
```

## ⚠️ **Consideraciones importantes:**

1. **Espacios en nombres**: Usa comillas si el archivo o carpeta tiene espacios
2. **Formato de ruta**: En Windows puedes usar `\` o `/`
3. **Permisos**: Asegúrate de tener acceso a la carpeta del archivo
4. **Tamaño**: Archivos muy grandes pueden tardar más en procesarse

## 🚀 **Próximo paso recomendado:**
Una vez que tengas algunos archivos de audio en `audio_samples/`, puedes probar el script con:
```bash
python music_analyzer.py "audio_samples/tu_archivo.mp3"
```
