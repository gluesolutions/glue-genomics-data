from glue.config import data_factory
from glue.core import Data
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

    if 'rnaseq' in file_name:
        metadata_index = 'Barcode'
        is_gene_expression = True
        is_ataq = False
    elif 'ataq' in file_name:
        metadata_index = 'sample_id'
        is_ataq = True
        is_gene_expression = False
    df_metadata = pd.read_csv(metadata_file, sep='\t').set_index(metadata_index)  # index is Barcode in one file and sample_id in the other
    df_metadata.columns = df_metadata.columns.str.lower()  # For consistency
    df_counts = pd.read_csv(matrix_file, sep='\t')
    if is_ataq:
        ataq_ids = df_counts.index.values
        chr = df_counts['chr']
        starts = df_counts['start']
        ends = df_counts['end']
        df_counts.drop(['peak_id', 'chr', 'start', 'end'], axis=1, inplace=True)
        ataq_ids_array = np.outer(ataq_ids, np.ones(df_counts.shape[1])).astype('int')
    counts_data = np.array(df_counts)
    if is_gene_expression:
        gene_numbers = [int(x[7:]) for x in df_counts.index.values]  # Not general
        gene_array = np.outer(gene_numbers, np.ones(df_counts.shape[1])).astype('int')  # Cast as int, not string to avoid limit on 1D categorical components

    def get_sex_encoding(x):
        sex = df_metadata.loc[x, 'sex']
        male_tags = ['Male', 'male', 'M', 'm']
        female_tags = ['Female', 'female', 'f', 'F']
        if sex in male_tags:
            return 0
        elif sex in female_tags:
            return 1
        else:
            raise Exception("Bad tag found in sex metadata")

    def get_diet_encoding(x):
        diet = df_metadata.loc[x, 'diet']
        lean_tags = ['10% fat + fiber']
        fat_tags = ['44% fat + fiber', '44% fat+ fiber']  # Random discrepancy in metadata
        if diet in lean_tags:
            return 0
        elif diet in fat_tags:
            return 1
        else:
            raise Exception("Bad tag found in diet metadata")

    def get_strain_encoding(x):
        strain = df_metadata.loc[x, 'strain']
        b6_tags = ['B6', 'C57BL_6J']
        cast_tags = ['CAST', 'CAST_EiJ']
        nzo_tags = ['NZO', 'NZO_HlLtJ']
        if strain in b6_tags:
            return 0
        elif strain in cast_tags:
            return 1
        elif strain in nzo_tags:
            return 2
        else:
            raise Exception("Bad tag found in strain metadata")

    sex = [get_sex_encoding(x) for x in df_counts.columns]
    diet = [get_diet_encoding(x) for x in df_counts.columns]
    strain = [get_strain_encoding(x) for x in df_counts.columns]

    sex_array = np.outer(np.ones(df_counts.shape[0]), sex).astype('int')
    diet_array = np.outer(np.ones(df_counts.shape[0]), diet).astype('int')
    strain_array = np.outer(np.ones(df_counts.shape[0]), strain).astype('int')

    data_name = matrix_file[-20:]  # Short name for dataset
    if is_gene_expression:
        return Data(counts=counts_data, gene_ids=gene_array,
                    sex=sex_array, diet=diet_array,
                    strain=strain_array, label=data_name)
    elif is_ataq:
        return [Data(counts=counts_data, ataq_peak_ids=ataq_ids_array,
                     sex=sex_array, diet=diet_array,
                     strain=strain_array, label=data_name),
                Data(ataq_peak_ids=ataq_ids,
                     chr=chr,
                     start=starts,
                     end=ends,
                     label='ataq_peaks')]
