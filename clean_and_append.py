import pandas as pd
import os

new_file = 'pqtl_final.csv'
clean_file = 'pqtl_final_clean.csv'

new = pd.read_csv(new_file)
new = new[new['rsid'].str.startswith('rs', na=False)]

if os.path.exists(clean_file):
    existing = pd.read_csv(clean_file)
    combined = pd.concat([existing, new])
else:
    combined = new

combined.to_csv(clean_file, index=False)
print(f"Combined: {len(combined)} rows, {combined['protein'].nunique()} proteins")
