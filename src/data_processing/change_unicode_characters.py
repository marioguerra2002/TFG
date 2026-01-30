import pandas as pd

file = "data/processed/merged_social_media.csv"

# Leer con encoding explícito
df = pd.read_csv(file, encoding='utf-8')
print(f"Archivo leído: {file} con {len(df)} filas.")

# Cambiar caracteres Unicode específicos
unicode_replacements = {
    '\u2018': "'",  # Left single quotation mark
    '\u2019': "'",  # Right single quotation mark
    '\u201c': '"',  # Left double quotation mark
    '\u201d': '"',  # Right double quotation mark
    '\u2013': '-',  # En dash
    '\u2014': '-',  # Em dash
    '\u2026': '...',  # Ellipsis
    '\u00a0': ' ',  # Non-breaking space
    '\u00ab': '"',  # Left-pointing double angle quotation mark «
    '\u00bb': '"',  # Right-pointing double angle quotation mark »
    '\u2039': "'",  # Single left-pointing angle quotation mark ‹
    '\u203a': "'",  # Single right-pointing angle quotation mark ›
    '\u201a': ',',  # Single low-9 quotation mark ‚
    '\u201e': '"',  # Double low-9 quotation mark „
}

def replace_unicode_characters(text):
  if pd.isna(text):  # Handle NaN values
    return text
  for unicode_char, replacement in unicode_replacements.items():
    text = text.replace(unicode_char, replacement)
  return text

# Apply replacement
df['text'] = df['text'].apply(replace_unicode_characters)

# Save with explicit encoding
df.to_csv(file, index=False, encoding='utf-8')
print(f"File saved: {file} with {len(df)} rows.")
print("Unicode character replacement completed.")