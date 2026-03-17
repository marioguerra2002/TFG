
import re
import unicodedata
from collections import Counter
import pandas as pd

INPUT_FILE = "data/processed/lemmatized_tweets_lg_no_stopwords.csv"
OUTPUT_FILE = "data/processed/lemmatized_tweets_lg_no_stopwords_party_detection.csv"
RUN_DIAGNOSTICS = True

# Diccionario actualizado 2026/2027
DICTIONARY_FILE = {
    "PP": ["pp", "partido popular", "feijoo", "ayuso", "tellado", "cuca gamarra", "juanma moreno", "aznar", "rajoy", "genova"],
    "PSOE": ["psoe", "partido socialista", "sanchez", "pedro sanchez", "zapatero", "illa", "salvador illa", "montero", "ferraz", "sanchismo"],
    "VOX": ["vox", "abascal", "santiago abascal", "buxade", "garriga", "bambu"],
    "SUMAR": ["sumar", "yolanda diaz", "urtasun", "monica garcia"],
    "PODEMOS": ["podemos", "unidas podemos", "belarra", "ione belarra", "irene montero"],
    "SALF": ["salf", "se acabo la fiesta", "alvise", "alvise perez"],
    "ERC": ["esquerra republicana", "erc", "rufian", "gabriel rufian", "junqueras"],
    "JUNTS": ["junts", "junts per catalunya", "puigdemont", "carles puigdemont"],
    "PNV": ["partido nacionalista vasco", "pnv", "andoni ortuzar", "ortuzar", "pradales"],
    "BILDU": ["eh bildu", "bildu", "otegi", "arnaldo otegi", "aizpurua"]
}

def normalize_text(text):
  # Normaliza el texto para mejorar la coincidencia de palabras clave,
  # eliminando acentos, convirtiendo a minúsculas y eliminando espacios extra.
  # Aunque se haya una lematizacion previa, esta normalización adicional puede ayudar a
  # mejorar la calidad de las coincidencias y evitar falsos negativos
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text

NORMALIZED_DICTIONARY = {
    party: [normalize_text(keyword) for keyword in keywords]
    for party, keywords in DICTIONARY_FILE.items()
}


def keyword_in_text(text, keyword):
    # Coincidencia por palabra/frase completa para evitar falsos positivos por subcadenas como podria ser "pp" dentro de "psoe".
    # Utilizamos lookaround para asegurar que el keyword no esté precedido ni seguido por caracteres de palabra.
    pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"
    return re.search(pattern, text) is not None


def get_mentioned_parties(text): # esto es lo que se aplica a cada tweet para extraer la lista de partidos mencionados
    """
    Devuelve una lista con TODOS los partidos mencionados en el texto.
    Si un partido tiene coincidencias, se añade a la lista.
    """
    normalized_text = normalize_text(text)
    mentioned = []

    for party, keywords in NORMALIZED_DICTIONARY.items():
        # Si al menos una palabra clave del partido está en el texto, cuenta como mencionado
        if any(keyword and keyword_in_text(normalized_text, keyword) for keyword in keywords):
            mentioned.append(party)

    return mentioned

def analyze_dictionary(df, keyword_hits_counter):
    print("\n" + "="*50)
    print("--- DIAGNÓSTICO DE DETECCIÓN DE PARTIDOS ---")
    print("="*50)
    print("Top 20 palabras clave más detectadas:")
    for (party, keyword), hits in keyword_hits_counter.most_common(20):
        print(f"  - [{party}] '{keyword}': {hits} aciertos")
    print("="*50 + "\n")

def main():
    df = pd.read_csv(INPUT_FILE, encoding="utf-8")
    if "text_filtered" not in df.columns:
        raise ValueError("Column 'text_filtered' not found in the input file.")
    print(f"✅ Input file read successfully: {INPUT_FILE} with {len(df)} rows.")

    new_rows = []
    keyword_hits = Counter()

    stats = {
        "sin_partido": 0,
        "un_partido": 0,
        "multi_partido": 0
    }

    # Procesamos fila por fila para aplicar la detección de partidos y
    # el desdoblamiento (en caso de múltiples partidos se crea una fila por cada partido mencionado)
    for _, row in df.iterrows():
        text = row["text_filtered"]
        mentioned_parties = get_mentioned_parties(text)

        # Para el diagnóstico: contamos qué palabras exactas hicieron match
        if RUN_DIAGNOSTICS:
            norm_text = normalize_text(text)
            for party, keywords in NORMALIZED_DICTIONARY.items():
                for kw in keywords:
                    if kw and keyword_in_text(norm_text, kw):
                        keyword_hits[(party, kw)] += 1

        if not mentioned_parties:
            # No menciona a nadie
            stats["sin_partido"] += 1
            new_row = row.to_dict()
            new_row["party"] = "None"
            new_rows.append(new_row)
        else:
            if len(mentioned_parties) == 1:
                stats["un_partido"] += 1
            else:
                stats["multi_partido"] += 1

            # Desdoblamiento: creamos una fila por cada partido mencionado
            for party in mentioned_parties:
                new_row = row.to_dict()
                new_row["party"] = party
                new_rows.append(new_row)

    # Crear nuevo DataFrame
    df_out = pd.DataFrame(new_rows)
    df_out.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"💾 Output file saved successfully: {OUTPUT_FILE}")
    print("\n📊 RESUMEN DE LA EXTRACCIÓN (Opción C):")
    print(f"  - Tweets originales: {len(df)}")
    print(f"  - Filas finales (tras duplicar): {len(df_out)}")
    print(f"  - Tweets sin menciones políticas explícitas: {stats['sin_partido']}")
    print(f"  - Tweets que mencionan a 1 solo partido: {stats['un_partido']}")
    print(f"  - Tweets que mencionan a MULTIPLES partidos: {stats['multi_partido']}")

    if RUN_DIAGNOSTICS:
        analyze_dictionary(df, keyword_hits)

if __name__ == "__main__":
    main()
