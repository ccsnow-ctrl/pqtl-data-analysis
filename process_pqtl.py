import pandas as pd
import gzip
import os

# proteins and their folders
proteins = {
    'APOE': 'APOE_P02649_OID30727_v1_Inflammation_II',
    'CLU': 'CLU_P10909_OID30732_v1_Inflammation_II',
    'CR1': 'CR1_P17927_OID30697_v1_Inflammation_II',
    'TREM2': 'TREM2_Q9NZC2_OID20731_v1_Inflammation'
}

all_results = []

for protein, folder in proteins.items():
    print(f"Processing {protein}...")
    for file in os.listdir(folder):
        if file.endswith('.gz'):
            filepath = os.path.join(folder, file)
            df = pd.read_csv(filepath, sep='\s+', compression='gzip')
            df['p_value'] = 10**(-df['LOG10P'])
            df_sig = df[df['p_value'] < 5e-8].copy()
            df_sig['protein'] = protein
            all_results.append(df_sig)
            
final = pd.concat(all_results)
final.to_csv('pqtl_significant.csv', index=False)
print(f"Done! {len(final)} significant results saved.")



