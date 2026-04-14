import synapseclient
import subprocess
import pandas as pd
import os
import glob
import shutil

TOKEN = 'YOUR_TOKEN_HERE'
TOP_N = 500

syn = synapseclient.login(authToken=TOKEN)

with open('synids_fixed.txt') as f:
    synids = [line.strip() for line in f if line.strip()]

print(f"Found {len(synids)} proteins to download")

all_results = []

for i, synid in enumerate(synids):
    print(f"\n[{i+1}/{len(synids)}] Downloading {synid}...")
    try:
        entity = syn.get(synid, downloadLocation='.')
        tarfile = entity.path
        protein_name = os.path.basename(tarfile).split('_')[0]
        subprocess.run(['tar', '-xf', tarfile], check=True)
        folder = tarfile.replace('.tar', '')
        protein_dfs = []
        for gz in glob.glob(os.path.join(folder, '*.gz')):
            df = pd.read_csv(gz, sep=r'\s+', compression='gzip')
            df['p_value'] = 10**(-df['LOG10P'])
            df['protein'] = protein_name
            protein_dfs.append(df)
        if protein_dfs:
            combined = pd.concat(protein_dfs)
            top = combined.nsmallest(TOP_N, 'p_value')
            top = top.drop(columns=['EXTRA', 'TEST'], errors='ignore')
            all_results.append(top)
            print(f"  -> kept top {len(top)} variants for {protein_name}")
        os.remove(tarfile)
        shutil.rmtree(folder)
        print(f"  -> cleaned up {protein_name}")
        if all_results:
            pd.concat(all_results).to_csv('pqtl_significant.csv', index=False)
            print(f"  -> progress saved")
    except Exception as e:
        print(f"  -> FAILED {synid}: {e}, skipping...")
        continue

final = pd.concat(all_results)
print(f"\nDone! {len(final)} total variants saved to pqtl_significant.csv")