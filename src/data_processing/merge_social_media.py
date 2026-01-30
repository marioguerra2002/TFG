import pandas as pd

import glob # To look for patterns in file names
import os 

files = glob.glob("data/raw/social_media/*.csv")

# Delete first empty files
counter_files_deleted = 0
for f in files:
  try:
    df_temp = pd.read_csv(f)
    if df_temp.empty:
      os.remove(f)
      counter_files_deleted += 1
  except:
    os.remove(f)
    counter_files_deleted += 1
if counter_files_deleted > 0:
  print(f"Se han eliminado {counter_files_deleted} archivos vacíos.")

# Take files again after deletion
files = glob.glob("data/raw/social_media/*.csv")
print(f"Archivos restantes para procesar: {len(files)}")

dfs = [ pd.read_csv(f) for f in files ] # Read all CSV files into DataFrames
df_merged = pd.concat(dfs, ignore_index=True) # Merge all DataFrames into one

df_merged.drop_duplicates(subset=["text"], inplace=True) # Remove duplicate tweets based on 'text' column
df_merged.reset_index(drop=True, inplace=True) # Reset indices to be consecutive
df_merged.to_csv("data/processed/merged_social_media.csv", index=False) # Save the merged DataFrame

