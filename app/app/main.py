from flask import Flask, render_template, request
import pandas as pd
import joblib
import requests
import os
import numpy as np
import plotly.express as px
import plotly.io as pio
from datetime import datetime

app = Flask(__name__)


# Cargar modelo pkl

MODEL_PATH = "models/model_rf.pkl"

with open(MODEL_PATH, "rb") as f:
    model = joblib.load(f)


# Cargar dataset limpio
DATA_PATH = "../data/velocidades_clean.parquet"
df = pd.read_parquet(DATA_PATH)


# APIKEY OpenWeatherMap
API_KEY = "2d766fc0630c60dec177b391207e3e91"
CITY = "Bogota,CO"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&lang=es&appid={API_KEY}"
    r = requests.get(url)
    data = r.json()

    if r.status_code != 200:
        return None

    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind": data["wind"]["speed"]
    }

## RUTAS FLASK ##
# Ruta principal
@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None
    weather = get_weather()

    if request.method == "POST":
        hora = int(request.form["hora"])
        distancia = float(request.form["distancia"])

        X = pd.DataFrame([[hora, distancia]], columns=["hora", "distancia"])
        result = model.predict(X)[0]

        prediction = round(result, 2)

    return render_template("index.html", prediction=prediction, weather=weather)



# Ruta Dashboard graficas
@app.route("/dashboard")
def dashboard():

    # 1. Velocidad por hora
    vel_hora = df.groupby("hora")["velocidad"].mean().reset_index()
    fig1 = px.line(vel_hora, x="hora", y="velocidad", title="Velocidad Promedio por Hora")
    graph1 = pio.to_html(fig1, full_html=False)

    # 2. Histograma general
    fig2 = px.histogram(df, x="velocidad", nbins=40, title="Distribución de Velocidades")
    graph2 = pio.to_html(fig2, full_html=False)

    # # 3. Heatmap día-hora (si existe columna DIA_SEMANA)
    # if "DIA_SEMANA" in df.columns:
    #     piv = df.pivot_table(values="velocidad", index="DIA_SEMANA", columns="hora", aggfunc="mean")
    #     fig3 = px.imshow(piv, title="Mapa de Congestión Día-Hora")
    #     graph3 = pio.to_html(fig3, full_html=False)
    # else:
    #     graph3 = "<p>No existe la columna DIA_SEMANA para generar heatmap.</p>"

    # 4. Clasificar congestión por origen
    df2 = df.copy()
    df2["estado"] = pd.cut(
        df2["velocidad"],
        bins=[0, 20, 30, 40, 200],
        labels=["🔴 Muy Congestionado", "🟡 Lento", "🔵 Normal", "🟢 Fluido"]
    )

    congest_list = df2.groupby("origen")["estado"].agg(lambda x: x.value_counts().index[0]).reset_index()

    return render_template(
        "dashboard.html",
        graph1=graph1,
        graph2=graph2,
        # graph3=graph3,
        congest_list=congest_list.to_dict(orient="records")
    )


if __name__ == "__main__":
    app.run(debug=True)
