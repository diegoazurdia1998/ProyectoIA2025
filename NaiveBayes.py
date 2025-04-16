# ruta datasetC:\Users\diego\Documents\1Universidad\IA\Proyecto\ProyectoIA2025\pariza\bbc-news-summary\versions\2\BBC News Summary\Summaries

# Imports
import os
import pandas as pd
import numpy as np
from collections import defaultdict
import re
from sklearn.model_selection import train_test_split

# Función para cargar datos
def load_data(base_path):
    categories = ["business", "entertainment", "politics", "sport", "tech"]
    data = []
    for category in categories:
        article_dir = os.path.join(base_path, "News Articles", category)
        for file in os.listdir(article_dir):
            with open(os.path.join(article_dir, file), "r", encoding="latin1") as f:
                text = f.read()
            data.append({"text": text, "category": category})
    return pd.DataFrame(data)

# Preprocesamiento: limpieza y tokenización
def preprocess(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    return text.split()

# Cargar y preprocesar datos
df = load_data("\pariza\bbc-news-summary\versions\2\BBC News Summary\Summaries")  # Cambia la ruta
df["tokens"] = df["text"].apply(preprocess)

# Dividir en 80% entrenamiento, 20% prueba (stratified para mantener proporción de clases)
X_train, X_test, y_train, y_test = train_test_split(
    df["tokens"],
    df["category"],
    test_size=0.2,
    random_state=42,
    stratify=df["category"]  # Importante para clases desbalanceadas
)


# Construir vocabulario solo con datos de entrenamiento
def build_vocabulary(tokens_list):
    vocabulary = defaultdict(int)
    for tokens in tokens_list:
        for token in tokens:
            vocabulary[token] += 1
    # Filtrar palabras raras (ejemplo: frecuencia mínima 3)
    vocabulary = {word: count for word, count in vocabulary.items() if count >= 3}
    return vocabulary


vocabulary = build_vocabulary(X_train)
word_index = {word: idx for idx, word in enumerate(vocabulary.keys())}


# Implementación de Naive Bayes Multinomial
class MultinomialNB:
    def __init__(self):
        self.prior = {}
        self.word_counts = {}
        self.class_totals = {}

    def fit(self, X, y):
        classes = np.unique(y)
        self.prior = {c: np.sum(y == c) / len(y) for c in classes}

        self.word_counts = {c: defaultdict(int) for c in classes}
        self.class_totals = {c: 0 for c in classes}

        for tokens, label in zip(X, y):
            for token in tokens:
                if token in word_index:
                    self.word_counts[label][token] += 1
                    self.class_totals[label] += 1

    def predict(self, X):
        predictions = []
        for tokens in X:
            posteriors = {}
            for c in self.prior:
                log_posterior = np.log(self.prior[c])
                for token in tokens:
                    if token in word_index:
                        # Suavizado Laplace (add-1)
                        count = self.word_counts[c].get(token, 0) + 1
                        total = self.class_totals[c] + len(word_index)
                        log_posterior += np.log(count / total)
                posteriors[c] = log_posterior
            predictions.append(max(posteriors, key=posteriors.get))
        return predictions


# Entrenar y evaluar
model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

if __name__ == "__main__":
    # Entrenar y evaluar el modelo
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Métricas de evaluación
    from sklearn.metrics import accuracy_score, classification_report

    print("\n🔍 **Resultados del Modelo**")
    print(f"Precisión: {accuracy_score(y_test, y_pred):.2f}")
    print("\n📊 Reporte de Clasificación:")
    print(classification_report(y_test, y_pred))

    # Ejemplo de predicción manual
    test_news = ["Apple announced a new iPhone today", "The football team won the championship"]
    test_tokens = [preprocess(text) for text in test_news]
    test_pred = model.predict(test_tokens)

    print("\n📰 **Predicciones de Ejemplo**")
    for text, pred in zip(test_news, test_pred):
        print(f"Noticia: '{text}' \n→ Categoría predicha: {pred}\n")