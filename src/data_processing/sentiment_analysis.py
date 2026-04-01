# script para analizar el sentimiento de los tweets y ver si hay alguna correlación con los partidos políticos detectados

import pandas as pd
from pysentimiento import create_analyzer # pysentimiento es una biblioteca de análisis de sentimiento que soporta múltiples idiomas, incluyendo español. Permite analizar el sentimiento de textos de manera sencilla y eficiente.
from tqdm import tqdm # tqdm es una biblioteca que proporciona una barra de progreso para loops en Python, lo que facilita el seguimiento del progreso de tareas largas como el análisis de sentimiento en un gran conjunto de datos

INPUT_FILE = "data/processed/lemmatized_tweets_lg_no_stopwords_party_detection.csv"
OUTPUT_FILE = "data/processed/tweets_sentiment_by_partyv2.csv"

def get_sentiment(text, analyzer):
  try:
    result = analyzer.predict(str(text)) # Utiliza el analizador de sentimiento para predecir el sentimiento del texto
    return pd.Series([
      result.output,
      result.probas['POS'],
      # tiene que ser asi porque el resultado de analyzer.predict es un objeto con una propiedad "probas"
      # que es un diccionario con las probabilidades de cada clase de sentimiento (POS, NEG, NEU)
      result.probas['NEG'],
      result.probas['NEU']
    ])
  except Exception as e:
    print(f"Error analyzing sentiment for text: {text}\nError: {e}")
    return pd.Series(["NEU", 0.0, 0.0, 0.0]) # Devuelve una serie con valores nulos en caso de error

def main():
  print("Cargando datos...")
  df = pd.read_csv(INPUT_FILE, encoding="utf-8")
  if "text_filtered" not in df.columns:
    raise ValueError("Column 'text_filtered' not found in the input file.")
  print(f"✅ Input file read successfully: {INPUT_FILE} with {len(df)} rows.")

  df_partidos = df[df["party"].notna()].copy() # Filtra solo los tweets que tienen un partido político asignado
  print(f"Analizando sentimiento de {len(df_partidos)} tweets con partido asignado...")

  print ("Cargando analizador de sentimiento...")
  analyzer = create_analyzer(task="sentiment", lang="es") # Crea un analizador de sentimiento para el idioma español utilizando pysentimiento
  print("✅ Analizador de sentimiento cargado correctamente.")

  print ("Analizando sentimiento de los tweets usando LA COLUMNA TEXT ORIGINAl por necesidad de conexto...")
  tqdm.pandas(desc = "Progreso del análisis de sentimiento") # Configura tqdm para mostrar una barra de progreso al aplicar funciones a columnas de DataFrames
  df_partidos[["sentiment", "proba_positive", "proba_negative", "proba_neutral"]] = df_partidos["text"].progress_apply(get_sentiment, analyzer=analyzer) # Aplica la función de análisis de sentimiento a la columna "text" del DataFrame, almacenando los resultados en nuevas columnas
  print("✅ Análisis de sentimiento completado.")

  df_partidos.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig") # Guarda el DataFrame resultante con los análisis de sentimiento en un nuevo archivo CSV
  print("\n" + "="*50)
  print("🎉 ANÁLISIS COMPLETADO")
  print(f"💾 Guardado con éxito en: {OUTPUT_FILE}")
  print("="*50)

if __name__ == "__main__":
    main()
