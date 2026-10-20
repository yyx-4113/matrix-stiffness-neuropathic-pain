#!/bin/bash
# Canonical download list for the matrix-stiffness x neuropathic-pain reanalysis.
# All URLs below were verified reachable from ftp.ncbi.nlm.nih.gov on 2026-10-21.
# Run from analysis/data/raw/

set -euo pipefail

BASE=https://ftp.ncbi.nlm.nih.gov/geo/series

# ---------------------------------------------------------------------------
# Layer 0 — stiffness-controlled training set (human HEK293A RNA-seq, FPKM)
# GSE98547: 4 genotypes (WT, RAP2A/B/C-tKO, LATS1/2-dKO, YAP/TAZ-dKO)
#           x 2 matrices (1 kPa soft, 40 kPa stiff) x 3 replicates = 24 samples
# ---------------------------------------------------------------------------
curl -O "$BASE/GSE98nnn/GSE98547/matrix/GSE98547_series_matrix.txt.gz"
curl -O "$BASE/GSE98nnn/GSE98547/suppl/GSE98547_RAW.tar"        # 39 MB, 24 x FPKM txt.gz
tar -xf GSE98547_RAW.tar
gzip -d -k GSM*.txt.gz

# ---------------------------------------------------------------------------
# Layer 1 — neuropathic / inflammatory pain (mouse, 36 samples)
# GSE111216: tissues BRN / SC / DRG / BLD
#            groups CTR, CFA (inflammatory), SNI (neuropathic), n = 3 each
# NOTE: this series deposits no sample-level expression matrix; the processed
#       data are 8 full-genome per-contrast differential-expression tables.
# ---------------------------------------------------------------------------
curl -O "$BASE/GSE111nnn/GSE111216/matrix/GSE111216_series_matrix.txt.gz"
for f in \
  GSE111216_Parisien_Suppl_Table_01_gene_BRN_CTRvsCFA.xlsx \
  GSE111216_Parisien_Suppl_Table_02_gene_BRN_CTRvsSNI.xlsx \
  GSE111216_Parisien_Suppl_Table_03_gene_SC_CTRvsCFA.xlsx \
  GSE111216_Parisien_Suppl_Table_04_gene_SC_CTRvsSNI.xlsx \
  GSE111216_Parisien_Suppl_Table_05_gene_DRG_CTRvsCFA.xlsx \
  GSE111216_Parisien_Suppl_Table_06_gene_DRG_CTRvsSNI.xlsx \
  GSE111216_Parisien_Suppl_Table_07_gene_BLD_CTRvsCFA.xlsx \
  GSE111216_Parisien_Suppl_Table_08_gene_BLD_CTRvsSNI.xlsx ; do
  curl -O "$BASE/GSE111nnn/GSE111216/suppl/$f"
done

echo "download complete"
