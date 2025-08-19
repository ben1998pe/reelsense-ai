#!/usr/bin/env python3
"""
Script de configuración para OpenRouter API
Ayuda a configurar la API key para generar TikTok reels
"""

import os
import sys

def setup_openrouter_api():
    """Configura la API key de OpenRouter."""
    print("🔑 CONFIGURACIÓN DE OPENROUTER API")
    print("=" * 50)
    
    print("📱 OpenRouter te permite acceder a modelos de IA como GPT-4, Claude, etc.")
    print("🎬 Con esto podrás generar conceptos virales para TikTok reels automáticamente!")
    print()
    
    # Verificar si ya está configurada
    current_key = os.getenv('OPENROUTER_API_KEY')
    if current_key:
        print(f"✅ API key ya configurada: {current_key[:8]}...")
        change = input("¿Quieres cambiarla? (s/n): ").lower().strip()
        if change != 's':
            print("Configuración mantenida.")
            return
    
    print("📋 PASOS PARA OBTENER TU API KEY:")
    print("1. Ve a https://openrouter.ai/")
    print("2. Crea una cuenta gratuita")
    print("3. Ve a 'API Keys' en tu dashboard")
    print("4. Crea una nueva API key")
    print("5. Copia la key generada")
    print()
    
    # Solicitar API key
    api_key = input("🔑 Ingresa tu API key de OpenRouter: ").strip()
    
    if not api_key:
        print("❌ No se ingresó ninguna API key.")
        return
    
    # Configurar para la sesión actual
    os.environ['OPENROUTER_API_KEY'] = api_key
    
    # Configurar para Windows (PowerShell)
    if sys.platform == "win32":
        print("\n🪟 Configurando para Windows...")
        print("Para hacer permanente, ejecuta este comando en PowerShell:")
        print(f'[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "{api_key}", "User")')
        
        # También configurar para la sesión actual de PowerShell
        os.system(f'set OPENROUTER_API_KEY={api_key}')
    
    # Configurar para Linux/Mac
    else:
        print("\n🐧 Configurando para Linux/Mac...")
        print("Para hacer permanente, agrega esta línea a tu ~/.bashrc o ~/.zshrc:")
        print(f'export OPENROUTER_API_KEY="{api_key}"')
        
        # También configurar para la sesión actual
        os.system(f'export OPENROUTER_API_KEY="{api_key}"')
    
    print(f"\n✅ API key configurada: {api_key[:8]}...")
    print("🎉 ¡Ahora puedes generar TikTok reels automáticamente!")
    
    # Probar la configuración
    test_configuration(api_key)

def test_configuration(api_key):
    """Prueba la configuración de la API key."""
    print("\n🧪 PROBANDO CONFIGURACIÓN...")
    
    try:
        import openai
        
        # Configurar cliente
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Hacer una llamada de prueba simple
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Di 'Hola' en español"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✅ Configuración exitosa! La API key funciona correctamente.")
            print(f"   Respuesta de prueba: {response.choices[0].message.content}")
        else:
            print("⚠️ La API key funciona pero no se recibió respuesta.")
            
    except Exception as e:
        print(f"❌ Error en la configuración: {str(e)}")
        print("💡 Verifica que la API key sea correcta y tengas créditos disponibles.")

def show_usage_examples():
    """Muestra ejemplos de uso."""
    print("\n📚 EJEMPLOS DE USO:")
    print("=" * 30)
    
    print("🎵 1. Análisis musical básico (sin TikTok):")
    print("   python src/music_analyzer_improved.py inputs/tu_cancion.mp3")
    
    print("\n🎬 2. Análisis + Generación de TikTok reels:")
    print("   python src/music_analyzer_with_tiktok.py inputs/tu_cancion.mp3")
    
    print("\n🎯 3. Generar múltiples conceptos:")
    print("   python src/music_analyzer_with_tiktok.py inputs/tu_cancion.mp3 --concepts 5")
    
    print("\n🔧 4. Usar modelo Whisper específico:")
    print("   python src/music_analyzer_with_tiktok.py inputs/tu_cancion.mp3 -m medium")
    
    print("\n💾 5. Guardar en archivo específico:")
    print("   python src/music_analyzer_with_tiktok.py inputs/tu_cancion.mp3 -o mi_analisis.json")

def main():
    """Función principal."""
    print("🎵🎬 REELSENSE AI - CONFIGURACIÓN DE OPENROUTER")
    print("=" * 60)
    
    while True:
        print("\n🔧 OPCIONES:")
        print("1. Configurar API key de OpenRouter")
        print("2. Ver ejemplos de uso")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            setup_openrouter_api()
        elif choice == "2":
            show_usage_examples()
        elif choice == "3":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
