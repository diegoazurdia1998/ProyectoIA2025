import kagglehub
import os

# Ruta personalizada para descarga (usa raw string 'r' para evitar errores con '\')
ruta_repositorio = r"C:\Users\diego\Documents\1Universidad\IA\Proyecto\ProyectoIA2025"

# Asegurar que la ruta exista
os.makedirs(ruta_repositorio, exist_ok=True)

# Descargar dataset
try:
    path = kagglehub.dataset_download(
        "pariza/bbc-news-summary"
    )
    print(f"✅ Dataset descargado en: {path}")
except Exception as e:
    print(f"❌ Error al descargar: {e}")