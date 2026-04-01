from collections import Counter
import pandas as pd

# Este script analiza los tweets que no han sido asignados a ningún partido político para descubrir posibles keywords
# ocultas que podrían ayudar a mejorar la detección en el futuro.
def descubrir_keywords_ocultas():
    # Cargar el archivo con las detecciones ya hechas
    print("Cargando datos...")
    df = pd.read_csv("data/processed/lemmatized_tweets_lg_no_stopwords_party_detection.csv")

    # Filtrar solo los que NO tienen partido
    df["party"] = df["party"].fillna("None")

    # Ahora el filtro sí funcionará
    df_none = df[df["party"] == "None"]

    print(f"✅ Analizando {len(df_none)} tweets sin asignar...")

    # Contar todas las palabras de esos tweets
    todas_las_palabras = " ".join(df_none["text_filtered"].dropna()).split()
    contador = Counter(todas_las_palabras)

    print("\n📈 Top 50 palabras más repetidas en tweets sin partido:")
    for palabra, frec in contador.most_common(50):
        # Ignoramos palabras de menos de 4 letras para limpiar ruido
        if len(palabra) > 3:
            print(f" - {palabra}: {frec}")

if __name__ == "__main__":
    descubrir_keywords_ocultas()
