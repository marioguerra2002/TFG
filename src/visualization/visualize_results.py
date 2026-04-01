import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "data/processed/tweets_sentiment_by_partyv2.csv"
OUTPUT_DIR = "data/visualizations"

os.makedirs(OUTPUT_DIR, exist_ok=True) # crear directorio si no está creado
PARTY_COLORS = {
  "PP": "#1D84CE",
  "PSOE": "#EF1C27",
  "VOX": "#63BE21",
  "SUMAR": "#E51C55",
  "PODEMOS": "#612B71",
  "SALF": "#000000", # Se Acabó la Fiesta (Suele usar negro/ardilla)
  "ERC": "#FFB232",
  "JUNTS": "#40E0D0",
  "PNV": "#008000",
  "BILDU": "#B2D234"
}

def share_voices (df): # funcion para generar gráfico de share of voice
  print ("Generar gráfico de share of voice...")
  sov = df['party'].value_counts().reset_index()
  sov.columns = ['Partido', 'Menciones']

  plt.figure(figsize=(10, 6))
  sns.barplot(
    data=sov,
    x='Menciones',
    y='Partido',
    hue='Partido',
    palette=PARTY_COLORS,
    dodge=False,
    legend=False
  )
  plt.title('Share of Voice (Volumen de Menciones por Partido)')
  plt.xlabel('Número de Menciones')
  plt.ylabel('')
  plt.tight_layout()
  plt.savefig(os.path.join(OUTPUT_DIR, "1_share_of_voice.png"), dpi=300)
  plt.close()
  return sov

def sentiment_distribution_graph(df):
  print ("Generar gráfico de distribución de sentimiento...")
  # --- GRÁFICO 2: DISTRIBUCIÓN DE SENTIMIENTO POR PARTIDO ---
  print("Generando gráfico de distribución de sentimiento...")
  # Calcular porcentajes de POS, NEG, NEU por partido
  sentiment_dist = df.groupby(['party', 'sentiment']).size().unstack(fill_value=0)
  # Convertir a porcentajes (del 0 al 100%)
  sentiment_dist = sentiment_dist.div(sentiment_dist.sum(axis=1), axis=0) * 100

  # Ordenar por el que tiene más sentimiento Negativo (para que el gráfico tenga sentido visual)
  sentiment_dist = sentiment_dist.sort_values(by='NEG', ascending=True)

  # Colores semánticos para los sentimientos
  color_map = {'POS': '#2ecc71', 'NEU': '#95a5a6', 'NEG': '#e74c3c'}

  sentiment_dist[['POS', 'NEU', 'NEG']].plot(
      kind='barh', stacked=True, figsize=(12, 7), color=[color_map[c] for c in ['POS', 'NEU', 'NEG']]
  )
  plt.title('Distribución del Sentimiento en Twitter por Partido (%)')
  plt.xlabel('Porcentaje (%)')
  plt.ylabel('Partido Político')
  plt.legend(title="Sentimiento", loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
  plt.tight_layout()
  plt.savefig(os.path.join(OUTPUT_DIR, "2_sentiment_distribution.png"), dpi=300)
  plt.close()

def net_sentiment_graph(sentiment_dist):
  print("Generando gráfico de Sentimiento Neto...")
  # Sentimiento Neto = % Positivo - % Negativo
  sentiment_dist['Sentimiento_Neto'] = sentiment_dist['POS'] - sentiment_dist['NEG']
  neto_df = sentiment_dist[['Sentimiento_Neto']].reset_index().sort_values(by='Sentimiento_Neto', ascending=False)

  plt.figure(figsize=(10, 6))
  # Barras verdes si es > 0, rojas si es < 0
  colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in neto_df['Sentimiento_Neto']]
  net_sentiment_palette = dict(zip(neto_df['party'], colors))

  sns.barplot(
    data=neto_df,
    x='Sentimiento_Neto',
    y='party',
    hue='party',
    palette=net_sentiment_palette,
    dodge=False,
    legend=False
  )
  plt.title('Sentimiento Neto por Partido (% Positivo - % Negativo)')
  plt.xlabel('Puntuación Neta')
  plt.ylabel('')

  # Añadir una línea vertical en el 0
  plt.axvline(0, color='black', linewidth=1.5, linestyle='--')

  plt.tight_layout()
  plt.savefig(os.path.join(OUTPUT_DIR, "3_net_sentiment.png"), dpi=300)
  plt.close()
  return neto_df

def main():
  print("Cargando datos...")
  df = pd.read_csv(INPUT_FILE, encoding="utf-8")
  if "party" not in df.columns or "sentiment" not in df.columns:
    raise ValueError("Columns 'party' and 'sentiment' must be present in the input file.")
  print(f"✅ Input file read successfully: {INPUT_FILE} with {len(df)} rows.")

  sov = share_voices(df)
  sentiment_distribution_graph(df)

  # Para el gráfico de sentimiento neto, necesitamos la distribución de sentimientos por partido
  sentiment_dist = df.groupby(['party', 'sentiment']).size().unstack(fill_value=0)
  sentiment_dist = sentiment_dist.div(sentiment_dist.sum(axis=1), axis=0) * 100
  neto_df = net_sentiment_graph(sentiment_dist)

  print("\n" + "="*50)
  print("🎯 RESUMEN ANALÍTICO PARA LA MEMORIA:")
  print("="*50)
  print("\n1. Top 3 Partidos más mencionados (Share of Voice):")
  for _, row in sov.head(3).iterrows():
    print(f"   - {row['Partido']}: {row['Menciones']} menciones")

  print("\n2. Ránking de Sentimiento Neto (El 'ganador' en Twitter):")
  for _, row in neto_df.iterrows():
    print(f"   - {row['party']}: {row['Sentimiento_Neto']:.2f} puntos")


if __name__ == "__main__":
  main()



