import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

# =======================
# Cargar dataset limpio
# =======================
df = pd.read_csv("data/velocidades_limpio.csv")

# =======================
# Ingeniería de características
# =======================
df["HORA"] = df["HORA"].astype(int)
df["DIA_SEMANA"] = df["DIA_SEMANA"].astype(int)
df["MES"] = df["MES"].astype(int)

# ===== Variables climáticas simuladas (por ahora) =====
# El modelo necesita clima aunque Flask lo traiga en tiempo real
np.random.seed(42)
df["TEMP"] = np.random.uniform(8, 20, len(df))
df["HUMEDAD"] = np.random.uniform(30, 90, len(df))
df["VIENTO"] = np.random.uniform(0, 7, len(df))

features = [
    "HORA", "DIA_SEMANA", "MES",
    "DISTANCE", "VEL_MEDIA_BRT", "VEL_MEDIA_MIXTO",
    "NUMDISPOSITIVOS", "TEMP", "HUMEDAD", "VIENTO"
]

X = df[features]
y = df["VEL_PROMEDIO"]

# =======================
# Separar entrenamiento
# =======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =======================
# Entrenar modelo
# =======================
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

model.fit(X_train, y_train)

print("Score del modelo:", model.score(X_test, y_test))

# =======================
# Guardar modelo
# =======================
with open("models/model_rf.pkl", "wb") as f:
    pickle.dump(model, f)

print("Modelo guardado en models/model_rf.pkl")
