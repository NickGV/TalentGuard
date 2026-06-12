"""
TalentGuard — Script de entrenamiento local reproducible.

Entrena Logistic Regression y Random Forest sobre los datos procesados,
selecciona el mejor modelo por F1-macro en test y serializa el pipeline
junto con sus métricas.

Uso:
    python src/ml/entrenar_modelo.py

Requisitos:
    - data/processed/ con X_train.csv, X_test.csv, y_train.csv, y_test.csv
    - Ejecutar dentro del entorno virtual activo (compatibilidad sklearn)
"""

import json
import joblib
import pandas as pd
import numpy as np
from datetime import date
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score,
    recall_score, roc_auc_score,
)

RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def cargar_datos():
    X_train = pd.read_csv(PROCESSED_DIR / "X_train.csv")
    X_test  = pd.read_csv(PROCESSED_DIR / "X_test.csv")
    y_train = pd.read_csv(PROCESSED_DIR / "y_train.csv").squeeze()
    y_test  = pd.read_csv(PROCESSED_DIR / "y_test.csv").squeeze()
    print(f"Train: {X_train.shape} | Test: {X_test.shape}")
    return X_train, X_test, y_train, y_test


def definir_modelos():
    return {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=RANDOM_STATE,
            )),
        ]),
        "Random Forest": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=100,
                class_weight="balanced",
                random_state=RANDOM_STATE,
            )),
        ]),
    }


def evaluar(pipeline, X_test, y_test):
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    return {
        "pipeline": pipeline,
        "y_pred":   y_pred,
        "accuracy":        round(accuracy_score(y_test, y_pred), 4),
        "f1_macro":        round(f1_score(y_test, y_pred, average="macro"), 4),
        "f1_yes":          round(f1_score(y_test, y_pred, pos_label=1), 4),
        "precision_macro": round(precision_score(y_test, y_pred, average="macro"), 4),
        "recall_macro":    round(recall_score(y_test, y_pred, average="macro"), 4),
        "roc_auc":         round(roc_auc_score(y_test, y_prob), 4),
    }


def entrenar_y_comparar(modelos, X_train, X_test, y_train, y_test):
    resultados = {}
    for nombre, pipeline in modelos.items():
        pipeline.fit(X_train, y_train)
        resultados[nombre] = evaluar(pipeline, X_test, y_test)
        m = resultados[nombre]
        print(f"  {nombre}: F1-macro={m['f1_macro']} | F1-Yes={m['f1_yes']} | AUC={m['roc_auc']}")
    return resultados


def serializar_modelo(pipeline, ruta):
    joblib.dump(pipeline, ruta)
    recargado = joblib.load(ruta)
    print(f"Modelo serializado y verificado: {ruta}")
    return recargado


def guardar_metadata(nombre, metricas, X_train, X_test):
    metadata = {
        "modelo":              nombre,
        "version":             "1.0",
        "fecha_entrenamiento": str(date.today()),
        "metrica_principal":   "f1_score_macro",
        "valor_metrica":       metricas["f1_macro"],
        "f1_yes":              metricas["f1_yes"],
        "accuracy":            metricas["accuracy"],
        "precision_macro":     metricas["precision_macro"],
        "recall_macro":        metricas["recall_macro"],
        "roc_auc":             metricas["roc_auc"],
        "variables_entrada":   X_train.columns.tolist(),
        "variable_objetivo":   "Attrition",
        "n_features":          X_train.shape[1],
        "train_size":          X_train.shape[0],
        "test_size":           X_test.shape[0],
        "class_weight":        "balanced",
        "observaciones":       (
            f"Pipeline: StandardScaler + {nombre}. "
            "class_weight='balanced' para desbalance 84/16. "
            "random_state=42."
        ),
    }
    ruta = MODELS_DIR / "model_metadata.json"
    with open(ruta, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Métricas guardadas: {ruta}")
    return metadata


def main():
    print("=== TalentGuard — Entrenamiento de Modelos ===\n")

    X_train, X_test, y_train, y_test = cargar_datos()
    modelos = definir_modelos()

    print("\nEntrenando modelos...")
    resultados = entrenar_y_comparar(modelos, X_train, X_test, y_train, y_test)

    mejor_nombre = max(resultados, key=lambda k: resultados[k]["f1_macro"])
    mejor = resultados[mejor_nombre]
    print(f"\nMejor modelo (F1-macro): {mejor_nombre} — {mejor['f1_macro']}")

    serializar_modelo(mejor["pipeline"], MODELS_DIR / "modelo_final.pkl")
    guardar_metadata(mejor_nombre, mejor, X_train, X_test)

    print("\n=== Entrenamiento completo ===")


if __name__ == "__main__":
    main()
