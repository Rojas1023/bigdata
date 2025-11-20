import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train():

    PARQUET_PATH = "../data/velocidades_clean.parquet" # Ruta del archivo parquet limpio
    MODEL_PATH = "../app/models/model_rf.pkl"

    if not os.path.exists(PARQUET_PATH):
        raise FileNotFoundError(f"No existe el {PARQUET_PATH}.")

    print("Cargando datos")

    df = pd.read_parquet(PARQUET_PATH)

    # Verificar columnas
    required = ["velocidad", "hora", "distancia"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    print("Entrenando modelo")

    X = df[["hora", "distancia"]]
    y = df["velocidad"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )

    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)

    print(f"Modelo entrenado correctamente: {score:.4f}")

    # Crear carpeta data si no existe
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    train()
