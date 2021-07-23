from glue.config import data_factory
from glue.core import Data
from pathlib import Path
import pandas as pd
import numpy as np


__all__ = ['is_matrix', 'read_matrix']


def is_matrix_counts(filename):
    return filename.endswith('_matrix_counts.txt')


def is_matrix_metadata(filename):
    return filename.endswith('_matrix_metadata.txt')


def is_matrix(filename, **kwargs):
    matrix_counts = is_matrix_counts(filename)
    matrix_metadata = is_matrix_metadata(filename)
    return matrix_counts or matrix_metadata




@data_factory('Matix data loader', is_matrix)
def read_matrix(file_name):
    """
    Read a matrix of results data into glue.

    Currently these are .txt files that look like
    *_matrix_counts.txt
    *_matrix_metadata.txt

    and we allow the user to select either one
    """
    if is_matrix_counts(file_name):
        matrix_file = file_name
        metadata_file = file_name.replace('counts', 'metadata')
    elif is_matrix_metadata(file_name):
        metadata_file = file_name
        matrix_file = file_name.replace('metadata', 'counts')
    
    print(f'metadata: {metadata_file}')
    print(f'matrix: {matrix_file}')

    df_metadata = pd.read_csv(metadata_file, sep='\t').set_index('Barcode')
    df_counts   = pd.read_csv(matrix_file, sep='\t')
    counts_data = np.array(df_counts)
    gene_number = [int(x[7:]) for x in df_counts.index.values] # Not general
    gene_array = np.outer(gene_number,np.ones(df_counts.shape[1])).astype('int')
    
    def get_sex_encoding(x):
        sex = df_metadata.loc[x,'Sex']
        male_tags = ['Male','male','M','m']
        female_tags = ['Female','female','f','F']
        if sex in male_tags:
            return 0
        elif sex in female_tags:
            return 1
        else:
            raise Exception("Bad tag found in sex metadata")
            
    def get_diet_encoding(x):
        diet = df_metadata.loc[x,'Diet']
        lean_tags = ['10% fat + fiber']
        fat_tags = ['44% fat + fiber']
        if diet in lean_tags:
            return 0
        elif diet in fat_tags:
            return 1
        else:
            raise Exception("Bad tag found in diet metadata")
            
    def get_strain_encoding(x):
        strain = df_metadata.loc[x,'Strain']
        b6_tags = ['B6']
        cast_tags = ['CAST']
        nzo_tags = ['NZO']
        if strain in b6_tags:
            return 0
        elif strain in cast_tags:
            return 1
        elif strain in nzo_tags:
            return 2
        else:
            raise Exception("Bad tag found in strain metadata")
            
    sex  = [get_sex_encoding(x) for x in df_counts.columns]
    diet = [get_diet_encoding(x) for x in df_counts.columns]
    strain = [get_strain_encoding(x) for x in df_counts.columns]
    
    sex_array = np.outer(np.ones(df_counts.shape[0]),sex).astype('int')
    diet_array = np.outer(np.ones(df_counts.shape[0]),diet).astype('int')
    strain_array = np.outer(np.ones(df_counts.shape[0]),strain).astype('int')
    
    return Data(counts=counts_data, genes=gene_array, 
                sex=sex_array, diet=diet_array, strain=strain_array,label=Path(file_name).stem)
