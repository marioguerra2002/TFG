import pandas as pd
import spacy
import os

INPUT_FILE = "data/processed/lemmatized_tweets_lg.csv"
OUTPUT_FILE = "data/processed/lemmatized_tweets_lg_no_stopwords.csv"

TEXT_COL = "text_lemma"

nlp = spacy.load("es_core_news_lg", disable=["parser", "ner"]) # Load the Spanish language model, disabling the parser and named entity recognizer for efficiency

stopwords = set(nlp.Defaults.stop_words) # Get the set of stop words from the language model

keep_words = { # Define a set of words to keep, even if they are in the stop words list
  "no", "nunca", "jamás", "sin", "ni",
  "muy", "más", "menos", "tan", "demasiado",
  "deber", "poder", "querer"
}

stopwords_to_remove = stopwords - keep_words # Calculate the set of stop words to remove by taking the difference

def remove_stopwords(text):
  if pd.isna(text):
    raise ValueError("Input text cannot be NaN.")

  tokens = text.split() # Split the input text into tokens
  filtered_tokens = []
  for token in tokens:
    token = token.strip()
    if token in stopwords_to_remove:
      continue # Skip tokens that are in the stop words to remove
    if len(token) <= 2 and token not in {"pp", "ps", "ue"}:
      # Keep short tokens that are in the exceptions set (political abbreviations)
      continue # Skip tokens that are 2 characters or shorter

    filtered_tokens.append(token) # Append the token to the list of filtered tokens
  return " ".join(filtered_tokens) # Join the filtered tokens back into a single string

def main():
  if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

  df = pd.read_csv(INPUT_FILE, encoding="utf-8")
  if TEXT_COL not in df.columns:
    raise ValueError(f"Column '{TEXT_COL}' not found in the input file.")
  print(f"Input file read successfully: {INPUT_FILE} with {len(df)} rows.")

  df["text_filtered"] = df[TEXT_COL].apply(remove_stopwords) # Apply the remove_stopwords function to the specified text column and create a new column for the filtered text



  df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8") # Save the processed DataFrame to a new CSV file
  print(f"Output file saved successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
  main()
  

