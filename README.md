Data loaders to get genomics data into Glue
===========================================

Currently includes loaders for :
1. BED (via pyranges)
2. BEDGRAPH (via astropy.table, but this is a bit slow) 
3. BEDPE (via pandas)
4. BigWig (via pyranges, but this is slow)
5. RNA-seq and ATAC-seq data matrices and metadata (code is very custom for specific test datafiles)
6. Peak Correlations data (from provided Excel spreadsheet)
