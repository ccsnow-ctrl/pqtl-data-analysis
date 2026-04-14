# pQTL Data Analysis

Protein quantitative trait locus (pQTL) analysis pipeline developed as part of **QTL-DB**, a cross-omics relational database project for BF768 Biological Databases (Boston University). This repository contains the data processing scripts used to download, filter, and annotate pQTL summary statistics from the UK Biobank Pharma Proteomics Project (UKB-PPP).

## Project context

QTL-DB is a relational database designed to organize and query QTL results across multiple omics layers (eQTL, pQTL, meQTL, metaboQTL) from large population cohorts including the Framingham Heart Study and UK Biobank. This pipeline handles the protein QTL component, contributing structured pQTL data to the shared database schema.

## What this pipeline does

The pipeline runs in four sequential steps:

**Step 1 — Download and process (`download_and_process.py`)**  
Connects to Synapse and downloads pQTL summary statistics for ~500 proteins from the UKB-PPP dataset. Each protein is distributed as a `.tar` archive containing one `.gz` file per chromosome. The script extracts each archive, computes p-values from LOG10P, keeps the top 500 most significant variants per protein, saves progress incrementally to `pqtl_significant.csv`, and cleans up raw files as it goes to manage disk space. Run with `nohup` as this takes a long time.

**Step 2 — Add rsIDs (`add_rsids.py`)**  
Reads the chromosomes present in `pqtl_significant.csv` and loads only the corresponding chromosome-specific rsID map files. Merges rsIDs and hg38 genomic positions (POS38) onto the significant hits by variant ID and outputs `pqtl_final.csv`.

**Step 3 — Clean and append (`clean_and_append.py`)**  
Filters `pqtl_final.csv` to rows with valid rsIDs (those beginning with `rs`), then appends the cleaned results to a running master file `pqtl_final_clean.csv`. This allows the pipeline to be run incrementally across batches of proteins.

**Step 4 — Filter proteins of interest (`process_pqtl.py`)**  
Filters results down to four Alzheimer's disease-relevant proteins: APOE, CLU, CR1, and TREM2. Recalculates p-values from LOG10P and saves significant associations (p < 5×10⁻⁸) for downstream analysis.

## Data

Raw data is not included in this repository due to file size. Summary statistics were downloaded from the **UK Biobank Pharma Proteomics Project (UKB-PPP)** via Synapse. A Synapse account and access approval are required.

- Synapse IDs for the downloaded proteins are listed in `synids_fixed.txt`
- rsID map files follow the naming convention: `olink_rsid_map_mac5_info03_b0_7_chr{CHROM}_patched_v2.tsv.gz`
- Reference: Sun et al., *Nature*, 2023 — Plasma proteomic associations with genetics and health in the UK Biobank

## Requirements

```
pandas
synapseclient
```

Install with:

```bash
pip install pandas synapseclient
```

## Usage

Before running, replace `YOUR_TOKEN_HERE` in `download_and_process.py` with your Synapse personal access token.

```bash
# 1. Download and filter (~500 proteins from Synapse, runs in background)
nohup python3 download_and_process.py > output.log 2>&1 &

# 2. Monitor progress
tail -f output.log

# 3. Add rsIDs and hg38 positions
python3 add_rsids.py

# 4. Clean and append to master file
python3 clean_and_append.py

# 5. Check disk space
df -h ~

# 6. Clean up intermediate files
rm pqtl_final.csv pqtl_significant.csv output.log
```

To filter for specific proteins of interest (e.g. AD-relevant proteins):

```bash
python3 process_pqtl.py
```

## Repository contents

```
├── download_and_process.py   # Download and filter UKB-PPP data from Synapse
├── add_rsids.py              # Annotate significant hits with rsIDs and hg38 positions
├── clean_and_append.py       # Filter valid rsIDs and append to master CSV
├── process_pqtl.py           # Filter to AD-relevant proteins (APOE, CLU, CR1, TREM2)
├── synids_fixed.txt          # Synapse IDs for downloaded proteins
└── README.md
```

## Contributors

This pipeline was developed by Christine Snow as part of a group project with Paul Okoro, Hannah Owen, Lauren Anderson, and Reem Rasmy, supervised by Dr. Xiaoling Zhang.
