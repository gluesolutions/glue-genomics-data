from glue.config import data_factory
from glue.core import Data
from pathlib import Path
from astropy.table import Table
import pandas as pd
import numpy as np


__all__ = ['is_peak_correlations', 'read_peak_correlations']


def is_peak_correlations(filename, **kwargs):
    return filename.endswith('.xlsx')


@data_factory('Peak Correlations (Excel)', is_peak_correlations)
def read_peak_correlations(file_name):
    """
    Read in the custom peak correlation Excel file provided by JAX.
    """
    df = pd.DataFrame(pd.read_excel(file_name))

    tab = Table.from_pandas(df) #read(file_name, format="ascii.csv")
    # tab.rename_column('\ufeffMm_chr', 'Mm_chr')

    new_tab = Table(names=('index', 'chrm', 'peak', 'corr'), 
                    dtype=(str, str, str, float))

    for row in tab:
        if isinstance(row['mm_gene.cor_with_peak'], np.ma.core.MaskedConstant):
            continue
    
        idx = row['Mm_Index']
        chrm = row['Mm_chr']
        genes = row['mm_gene.cor_with_peak'].split(',')
        genes = [x.split(':') for x in genes]

        for gene in genes:
            if len(gene) != 2:
                continue

            peak, corr = gene[0], float(gene[1])
            new_tab.add_row([idx, chrm, peak, corr])

    return Data(**{k: new_tab[k] for k in new_tab.colnames},
                label=Path(file_name).stem)
