# 📰 Clasificador de Noticias con Naive Bayes
### Descripción:
Este proyecto implementa un clasificador de noticias utilizando el algoritmo Naive Bayes Multinomial, diseñado para categorizar artículos de texto en 5 temas: business, entertainment, politics, sport y tech. El modelo aprende patrones de palabras desde un dataset de noticias de la BBC y predice la categoría de nuevos textos con alta precisión.

# ⚙️ Funcionamiento
### 1. Flujo del Programa
#### Carga de Datos:
    Lee los archivos de noticias desde la carpeta BBC News Summary/News Articles.
    Cada artículo se etiqueta automáticamente según su subdirectorio (ej: /business/ → clase "business").

#### Preprocesamiento:

    Limpieza: Elimina caracteres especiales y convierte el texto a minúsculas.
    Tokenización: Divide el texto en palabras individuales.
    Filtrado: Remueve palabras con frecuencia menor a 3 (para reducir ruido).
    
#### Entrenamiento:

    Calcula:
    - Probabilidades a priori (P(clase)).

    - Frecuencias de palabras por clase (P(palabra|clase)).

    - Aplica suavizado Laplace para evitar probabilidades cero.

#### Predicción:

    Dado un nuevo texto, el modelo:
    - Lo tokeniza y filtra.
    - Calcula la probabilidad logarítmica para cada clase.
    - Selecciona la clase con mayor probabilidad.

#### Evaluación:

    Genera un reporte con métricas: accuracy, precision, recall y *F1-score*.