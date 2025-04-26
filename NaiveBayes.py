import os
import sys
import re
import csv
import json
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np

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

# Ruta relativa al dataset
BASE_PATH = os.path.join(os.path.dirname(__file__), "pariza", "bbc-news-summary", "versions", "2", "BBC News Summary")
PROBABILITIES_FILE = os.path.join(os.path.dirname(__file__), "Data.csv")

# Cargar y preprocesar datos
df = load_data(BASE_PATH)
df["tokens"] = df["text"].apply(preprocess)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    df["tokens"], df["category"],
    test_size=0.2, random_state=42, stratify=df["category"]
)

# Construir vocabulario
def build_vocabulary(tokens_list):
    vocabulary = defaultdict(int)
    for tokens in tokens_list:
        for token in tokens:
            vocabulary[token] += 1
    return {word: count for word, count in vocabulary.items() if count >= 3}

vocabulary = build_vocabulary(X_train)
word_index = {word: idx for idx, word in enumerate(vocabulary.keys())}

# Función para cargar probabilidades desde Data.csv
def load_probabilities():
    probabilities = {}
    if os.path.exists(PROBABILITIES_FILE):
        with open(PROBABILITIES_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar encabezado
            for row in reader:
                label = row[0]
                probability = float(row[1])
                probabilities[label] = probability
    return probabilities

# Guardar probabilidades
def save_probabilities(priors):
    # Asegúrate de que la ruta existe
    os.makedirs(os.path.dirname(PROBABILITIES_FILE), exist_ok=True)  # ✅ asegurarse que el directorio exista
    with open(PROBABILITIES_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Clase", "Probabilidad"])
        for label, prob in priors.items():
            writer.writerow([label, prob])


# Modelo Naive Bayes
class MultinomialNB:
    def __init__(self):
        self.prior = load_probabilities()
        self.word_counts = {}
        self.class_totals = {}

    def fit(self, X, y):
        classes = np.unique(y)
        self.word_counts = {c: defaultdict(int) for c in classes}
        self.class_totals = {c: 0 for c in classes}
        class_counts = defaultdict(int)

        for tokens, label in zip(X, y):
            class_counts[label] += 1
            for token in tokens:
                if token in word_index:
                    self.word_counts[label][token] += 1
                    self.class_totals[label] += 1

        total = sum(class_counts.values())
        self.prior = {c: class_counts[c] / total for c in classes}
        save_probabilities(self.prior)

    def predict(self, X):
        predictions = []
        for tokens in X:
            posteriors = {}
            for c in self.prior:
                log_posterior = np.log(self.prior.get(c, 1e-9))
                for token in tokens:
                    if token in word_index:
                        count = self.word_counts[c].get(token, 0) + 1
                        total = self.class_totals[c] + len(word_index)
                        log_posterior += np.log(count / total)
                posteriors[c] = log_posterior
            best_class = max(posteriors, key=posteriors.get)
            predictions.append(best_class)

            # Guardar texto si es clasificado correctamente
            if len(sys.argv) > 1:
                original_text = sys.argv[1]
                target_dir = os.path.join(BASE_PATH, "News Articles", best_class)
                if os.path.isdir(target_dir):
                    file_count = len(os.listdir(target_dir)) + 1
                    file_path = os.path.join(target_dir, f"input_{file_count}.txt")
                    with open(file_path, 'w', encoding='latin1') as f:
                        f.write(original_text)

        return predictions

# Ejecución principalg
if __name__ == "__main__":
    def main():
        model = MultinomialNB()
        model.fit(X_train, y_train)

        if len(sys.argv) > 1:
            input_text = sys.argv[1]
            input_tokens = [preprocess(input_text)]
            pred = model.predict(input_tokens)
            print(pred[0])
        else:
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            output = {
                "accuracy": round(acc, 2),
                "report": report
            }
            print(json.dumps(output))

    main()
