import pandas as pd
import langid

# Input and output file paths
INPUT_FILE = "data/processed/merged_social_media.csv"
OUTPUT_FILE = "data/processed/merged_social_media_lang.csv"
OUTPUT_FILE_SPANISH = "data/processed/merged_social_media_es.csv"


def detect_language(text: str):
  # Handle null or empty values
  if pd.isna(text) or not str(text).strip():
    return "unk", 0.0

  # Clean text and check minimum length
  cleaned_text = str(text).replace("\n", " ").strip()
  if len(cleaned_text) < 10:
    return "unk", 0.0

  # Detect language using langid
  try:
    language_code, confidence = langid.classify(cleaned_text)
    return language_code, float(confidence)
  except Exception:
    return "unk", 0.0


def main():
  # Load the merged dataset
  df = pd.read_csv(INPUT_FILE, encoding="utf-8")
  print(f"Loaded file: {INPUT_FILE} ({len(df)} rows)")

  # Detect language for each tweet
  df[["language", "language_score"]] = df["text"].apply(
    lambda x: pd.Series(detect_language(x))
  )

  # Filter to keep only Spanish tweets
  df_spanish = df[df["language"] == "es"].copy()

  # Display language distribution statistics
  print("\nLanguage distribution (top 20):")
  print(df["language"].value_counts().head(20))

  print(f"\nSpanish tweets: {len(df_spanish)}")

  # Save output files
  df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
  df_spanish.to_csv(OUTPUT_FILE_SPANISH, index=False, encoding="utf-8-sig")

  print("\nOutput files saved:")
  print(f"  - All languages: {OUTPUT_FILE}")
  print(f"  - Spanish only: {OUTPUT_FILE_SPANISH}")


if __name__ == "__main__":
  main()
