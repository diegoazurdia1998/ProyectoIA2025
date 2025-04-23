import os
import sys
import pandas as pd
import numpy as np
from collections import defaultdict
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json
from sklearn.metrics import classification_report

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

# 📁 Ruta relativa al dataset desde la ubicación del script actual
BASE_PATH = os.path.join(os.path.dirname(__file__), "pariza", "bbc-news-summary", "versions", "2", "BBC News Summary")

# Cargar y preprocesar datos
df = load_data(BASE_PATH)
df["tokens"] = df["text"].apply(preprocess)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    df["tokens"],
    df["category"],
    test_size=0.2,
    random_state=42,
    stratify=df["category"]
)

# Construir vocabulario
def build_vocabulary(tokens_list):
    vocabulary = defaultdict(int)
    for tokens in tokens_list:
        for token in tokens:
            vocabulary[token] += 1
    vocabulary = {word: count for word, count in vocabulary.items() if count >= 3}
    return vocabulary

vocabulary = build_vocabulary(X_train)
word_index = {word: idx for idx, word in enumerate(vocabulary.keys())}

# Modelo Naive Bayes
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
                        count = self.word_counts[c].get(token, 0) + 1
                        total = self.class_totals[c] + len(word_index)
                        log_posterior += np.log(count / total)
                posteriors[c] = log_posterior
            predictions.append(max(posteriors, key=posteriors.get))
        return predictions


# ✅ Si se ejecuta directamente
if __name__ == "__main__":
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