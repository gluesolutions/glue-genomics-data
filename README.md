Data loaders to get genomics data into Glue
===========================================

Currently includes loaders for :
1. BED (via pyranges)
2. BEDGRAPH (custom tiling)
3. BEDPE (custom tiling)
4. BigWig (via pyranges, but this is slow)
5. RNA-seq and ATAC-seq data matrices and metadata (code is very custom for specific test datafiles)
6. Peak Correlations data (from provided Excel spreadsheet)
7. STL files providing a 3D model downloaded from [3D-GNOME](https://3dgnome.cent.uw.edu.pl)
