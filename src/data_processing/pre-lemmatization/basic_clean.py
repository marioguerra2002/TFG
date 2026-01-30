# basic clean previous to lemmatization

import pandas as pd

file = "data/processed/merged_social_media.csv"
# Read with explicit encoding
df = pd.read_csv(file, encoding='utf-8')
print(f"File read: {file} with {len(df)} rows.")

# all to lowercase
df['text'] = df['text'].str.lower()
# remove URLs
df['text'] = df['text'].str.replace(r'http\S+|www\S+|https\S+', '', case=False, regex=True)
# remove mentions
df['text'] = df['text'].str.replace(r'@\w+', '', case=False, regex=True)
# remove hashtags without removing the text (just the # symbol)
df['text'] = df['text'].str.replace(r'#', '', regex=True)
# normalize whitespace
df['text'] = df['text'].str.replace(r'\s+', ' ', regex=True).str.strip()
# remove invisible characters
df['text'] = df['text'].str.replace(r'[\r\n\t]+', ' ', regex=True).str.strip()

# Save with explicit encoding
df.to_csv(file, index=False, encoding='utf-8')
print(f"File saved: {file} with {len(df)} rows.")
print("Basic cleaning completed.")
