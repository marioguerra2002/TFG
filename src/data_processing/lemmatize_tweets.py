import os
import re
import spacy #
import pandas as pd

INPUT_FILE = "data/processed/merged_social_media_es.csv"
OUTPUT_FILE = "data/processed/lemmatized_tweets.csv"


TEXT_COL = "text"

URL_RE = re.compile(r"http\S+|www\S+|https\S+", re.IGNORECASE)
# This regex matches mentions in the format @username, where "username"
# consists of word characters (letters, digits, and underscores).
# The re.IGNORECASE flag makes the matching case-insensitive.
MENTION_RE = re.compile(r"@\w+", re.IGNORECASE)
# This regex matches hashtags in the format #hashtag, where "hashtag"
# consists of word characters (letters, digits, and underscores).
# The re.IGNORECASE flag makes the matching case-insensitive.


# This function checks if the input text is NaN (Not a Number) using pandas'
# isna() function.
def save_text(text: str) -> str:
  if pd.isna(text):
    return ""
  return str(text)


# Limpieza extra de normalizacion
# (aunque no es estrictamente necesaria, ayuda a mejorar la calidad de los datos)

def extra_light_normalize(text: str) -> str:
  text = text.replace("\n", " ").strip() # Replace newline characters with space
  text = URL_RE.sub("", text) # Remove URLs
  text = MENTION_RE.sub("", text) # Remove mentions
  text = re.sub(r"\s+", " ", text).strip()
  return text


# Function to lemmatize a document using spaCy
def lemmatize_doc(doc) -> tuple[str, str]:
  lemmas = [] # List to store the lemmatized tokens
  for t in doc:
    if t.is_space or t.is_punct: # Skip spaces and punctuation
      continue
    lemma = t.lemma_.strip().lower()
    # Get the lemma, strip whitespace, and convert to lowercase

    # If the lemma is empty or a pronoun placeholder,
    # use the original token text instead
    if lemma in ("", "-pron-"):
      lemma = t.text.strip().lower()

    # If the lemma is still empty after stripping, skip it
    if lemma == "":
      continue

    lemmas.append(lemma) # Append the lemma to the list of lemmas

  text_lemma = " ".join(lemmas) # Join the lemmas into a single string
  lemma_tokens = "|".join(lemmas) # Join the lemmas with '|' as a separator
  return text_lemma, lemma_tokens

def main():
  if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

  df = pd.read_csv(INPUT_FILE, encoding="utf-8")
  if TEXT_COL not in df.columns:
    raise ValueError(f"Column '{TEXT_COL}' not found in the input file.")
  print(f"Input file read successfully: {INPUT_FILE} with {len(df)} rows.")

  # Charge spacy

  nlp = spacy.load("es_core_news_md", disable=["ner"])
  # Load the Spanish language model, disabling the named entity recognition component for faster processing
  nlp.max_length = 2000000 # Increase the maximum document length to handle long tweets

  texts = df[TEXT_COL].apply(save_text).apply(extra_light_normalize).tolist() # Clean and normalize the text column, then convert to a list

  text_lemmas = [] # List to store the lemmatized text
  lemma_tokens_list = [] # List to store the lemma tokens


  batch_size = 256 # Process tweets in batches to optimize performance
  for i, doc in enumerate(nlp.pipe(texts, batch_size=batch_size)):
    text_lemma, lemma_tokens = lemmatize_doc(doc) # Lemmatize the document
    text_lemmas.append(text_lemma) # Append the lemmatized text to the list
    lemma_tokens_list.append(lemma_tokens) # Append the lemma tokens to the list

    # Print progress every 2000 tweets
    if (i + 1) % 1500 == 0:
      print(f"Processed {i + 1} / {len(texts)} tweets...")

  df["text_lemma"] = text_lemmas # Add the lemmatized text as a new column in the DataFrame
  df["lemma_tokens"] = lemma_tokens_list # Add the lemma tokens as a new column in the DataFrame

  #save
  df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8") # Save the DataFrame to a new CSV file with UTF-8 encoding
  print(f"Output file saved: {OUTPUT_FILE} with {len(df)} rows.")

if __name__ == "__main__":
  main()





