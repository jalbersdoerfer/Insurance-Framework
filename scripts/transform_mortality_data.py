from pathlib import Path
import pandas as pd

"""
Convert the Destatis period life table (GENESIS 12621-0001) to a tidy CSV containing:
'age', 'qx_male', 'qx_female'

Source: 
Destatis, Sterbetafel (Periodensterbetafel), Deutschland, Jahre, Geschlecht, Vollendetes Alter.

The script extracts mortality probabilities (qx) for males and females.
"""

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "12621-0001"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "mortality_table.csv"

AGE_COL = 1
QX_MALE_COL = 2
QX_FEMALE_COL = 16

# Read csv 
df_raw = pd.read_csv(RAW_DATA_PATH, sep=';', skiprows=9, header=None,
                     usecols=[AGE_COL, QX_MALE_COL, QX_FEMALE_COL], 
                     encoding='utf-8-sig', dtype='string')
df_raw.columns = ['age_raw', 'qx_male_raw', 'qx_female_raw']

# Extract age 
df = pd.DataFrame()

df['age'] = pd.to_numeric(df_raw['age_raw'].str.strip().str
                          .extract(r'^(\d+)\s+Jahr(?:e)?$', expand=False), errors='coerce')

# Convert mortality probabilities
df["qx_male"] = pd.to_numeric(df_raw["qx_male_raw"].str.strip().str
                              .replace(",", ".", regex=False), errors="coerce")

df["qx_female"] = pd.to_numeric(df_raw["qx_female_raw"].str.strip()
                                .str.replace(",", ".", regex=False), errors="coerce")

# Remove empty rows (keep only rows containing an actual age)
df = df.dropna(subset=['age']).copy()
df['age'] = df['age'].astype(int)

# Check for missing mortality probabilities.
if df[['qx_male', 'qx_female']].isna().any().any():
    raise ValueError('Missing or invalid mortality probabilities detected.')

# Check for duplicate ages.
if df['age'].duplicated().any():
    raise ValueError('Duplicate age values detected.')

# Check if all ages are present.
expected_ages = list(range(df['age'].min(), df['age'].max() + 1))
if sorted(df['age'].tolist()) != expected_ages:
    raise ValueError('Missing or discontinuous age values detected.')

# Check whether mortality probabilities are within [0, 1].
for column in ["qx_male", "qx_female"]:
    if not df[column].between(0, 1).all():
        raise ValueError(f"Invalid mortality probabilities in {column}.")

# Sort data
df = df.sort_values('age').reset_index(drop=True)

# Export csv
df.to_csv(OUTPUT_PATH, sep=",", index=False, encoding="utf-8", float_format="%.8f")





























