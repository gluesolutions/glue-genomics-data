from glue.config import data_factory
from glue.core import Data
import pandas as pd
import numpy as np
from pathlib import Path
from glue_genomics_viewers.heatmap.heatmap_coords import HeatmapCoords


__all__ = ['is_matrix', 'read_matrix', 'df_to_data']

def df_to_data(obj,label=None):
    result = Data(label=label)
    for c in obj.columns:
        result.add_component(obj[c], str(c))
    return result

def is_matrix_counts(filename):
    return '_matrix_counts' in filename


def is_matrix_metadata(filename):
    return '_matrix_metadata' in filename

def is_gene_metadata(filename):
    return 'geneInfo' in filename


def is_matrix(filename, **kwargs):
    matrix_counts = is_matrix_counts(filename)
    matrix_metadata = is_matrix_metadata(filename)
    gene_metadata = is_gene_metadata(filename)
    return matrix_counts or matrix_metadata or gene_metadata


@data_factory('Matix data loader', is_matrix, priority=999)
def read_matrix(file_name):
    """
    Read a matrix of results data into glue.

    Currently these are .txt files that look like
    *_matrix_counts.txt
    *_matrix_metadata.txt
    *_geneInfo.txt
    """
    if 'rnaseq' in file_name:
        label = 'gene_expression'
    if is_matrix_counts(file_name):
        df_counts = pd.read_csv(file_name, sep='\t').set_index('gene.id')
        counts_data = np.array(df_counts)
        
        # Cast as int, not string for performance reasons
        gene_numbers = [int(x[7:]) for x in df_counts.index.values]  # Not very general
        gene_array = np.outer(gene_numbers, np.ones(df_counts.shape[1])).astype('int')

        experiment_id = [int(x[5:]) for x in df_counts.columns]
        experiment_array = np.broadcast_to(experiment_id,df_counts.shape).astype('int')

        gene_labels = np.array(gene_numbers) #df_counts.index is proper, but these are way too long
        exp_labels = np.array(experiment_id) #df_counts.columns is proper, but a bit too long
    
        d1 = Data(counts=counts_data, 
             gene_ids=gene_array, 
             exp_ids=experiment_array,
             label=label,
             coords=HeatmapCoords(n_dim=2, x_axis_ticks=exp_labels, y_axis_ticks=gene_labels, labels=['Experiment ID','Gene ID']))
        return d1
    elif is_matrix_metadata(file_name):

        df_metadata = pd.read_csv(file_name, sep='\t')
        df_metadata.columns = df_metadata.columns.str.lower()  # For consistency
        df_metadata['orsam_id'] = [int(x[5:]) for x in df_metadata['barcode']]
        
        d2 = df_to_data(df_metadata,label=f'{label}_experiment_metadata')
        return d2
    elif is_gene_metadata(file_name):
        df_gene_table = pd.read_csv(file_name, sep='\t').set_index('gene.id')
        df_gene_table['gene_ids'] = [int(x[7:]) for x in df_gene_table.index.values]
        df_gene_table['chr'] = 'chr'+df_gene_table['chr'].astype(str)
        df_gene_table['start'] = (df_gene_table['start']*100_000).astype(int)
        df_gene_table['end'] = (df_gene_table['end']*100_000).astype(int)
        df_gene_table['middle'] = (df_gene_table['middle']*100_000).astype(int)
        d3 = df_to_data(df_gene_table,label=f"{label}_gene_metadata")
        return d3
        