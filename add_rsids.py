import pandas as pd
import gzip
import os

# load significant results
df = pd.read_csv('pqtl_significant.csv')

# get unique chromosomes 
chroms = df['CHROM'].unique()
print(f"Chromosomes needed: {chroms}")

# load only the rsid map files we need
rsid_maps = []
for chrom in chroms:
    fname = f'olink_rsid_map_mac5_info03_b0_7_chr{chrom}_patched_v2.tsv.gz'
    if os.path.exists(fname):
        tmp = pd.read_csv(fname, sep='\t', compression='gzip', usecols=['ID', 'rsid', 'POS38'])
        rsid_maps.append(tmp)
        print(f"Loaded chr{chrom} rsid map")

rsid_df = pd.concat(rsid_maps)

# merge
df_merged = df.merge(rsid_df, on='ID', how='left')
df_merged.to_csv('pqtl_final.csv', index=False)
print(f"Done! {len(df_merged)} rows saved to pqtl_final.csv")


