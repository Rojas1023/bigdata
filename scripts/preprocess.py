import pandas as pd
import os
from tqdm import tqdm

def process():

    INPUT_CSV = "../data/Velocidades_Bitcarrier_Octubre_2022.csv"
    OUTPUT_PARQUET = "../data/velocidades_clean.parquet" # Nombre del archivo limpio

    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(
            f"No se encontro {INPUT_CSV}. Asegurar de que el archivo está en la carpeta data"
        )

    print("Archivo encontrado. Iniciando limpieza")


    # Lectura (para CSV grandes)
    chunks = pd.read_csv(INPUT_CSV, chunksize=100000)
    cleaned_chunks = []

    print("Procesando datos en chunks")

    for chunk in tqdm(chunks):

        # Renombrado de columnas
        mapping = {
            "VEL_PROMEDIO": "velocidad",
            "HORA": "hora",
            "NAME_FROM": "origen",
            "NAME_TO": "destino",
            "DISTANCE": "distancia",
            "NUMDISPOSITIVOS": "num_dispositivos",
            "INICIO": "inicio",
            "FIN": "fin",
            "TID": "id_tramo",
            "Shape__Length": "longitud"
        }

        # Renombrar columnas que existan
        real_mapping = {k: v for k, v in mapping.items() if k in chunk.columns}

        print("Mapping detectado:", real_mapping)

        chunk = chunk.rename(columns=real_mapping)

        # Seleccionamos solo columnas de interés (las que existen)
        keep_cols = [
            "velocidad", "hora", "distancia", "origen", "destino",
            "num_dispositivos", "inicio", "fin", "id_tramo", "longitud"
        ]
        cols_present = [c for c in keep_cols if c in chunk.columns]

        chunk = chunk[cols_present]

        # Limpieza basica
        chunk = chunk.dropna()

        cleaned_chunks.append(chunk)

    # Unir todos los chunks listos
    df_all = pd.concat(cleaned_chunks, ignore_index=True)

    print("Guardando versión limpia en parquet")

    df_all.to_parquet(OUTPUT_PARQUET, index=False)

    print(f"Archivo limpio generado correctamente en: {OUTPUT_PARQUET}")


if __name__ == "__main__":
    process()
