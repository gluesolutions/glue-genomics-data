Data loaders to get genomics data into Glue
===========================================

Currently includes loaders for :
1. Hi-C and ChIA-PET (via strawC)
2. BED (via pyranges)
3. BEDGRAPH (via astropy.table, but this is a bit slow) 
4. BEDPE (via pandas)
5. BigWig (via pyranges, but this is slow)
6. RNA-seq and ATAC-seq data matrices and metadata (code is very custom for specific test datafiles)
7. Peak Correlations data (from provided Excel spreadsheet)
