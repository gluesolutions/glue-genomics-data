from glue.config import data_factory
from glue.core import Data
import pandas as pd
import numpy as np
from pathlib import Path


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
        is_atac = False
    elif 'atac' in file_name or 'ataq' in file_name:
        metadata_index = 'sample_id'
        is_atac = True
        is_gene_expression = False
    # index is Barcode in one file and sample_id in the other
    df_metadata = pd.read_csv(metadata_file, sep='\t')#.set_index(metadata_index)
    df_metadata.columns = df_metadata.columns.str.lower()  # For consistency
    df_counts = pd.read_csv(matrix_file, sep='\t')
    if is_atac:
        df_counts = df_counts[df_counts['chr']==3]
        atac_ids = df_counts.index.values
        chr = df_counts['chr']
        starts = df_counts['start']
        ends = df_counts['end']
        df_counts.drop(['peak_id', 'chr', 'start', 'end'], axis=1, inplace=True)
        atac_ids_array = np.outer(atac_ids, np.ones(df_counts.shape[1])).astype('int')
        experiment_id = [int(x[:4]) for x in df_counts.columns]
        experiment_array = np.broadcast_to(experiment_id,df_counts.shape).astype('int')
        df_metadata['sample_id'] = [int(x[:4]) for x in df_metadata['sample_id']]
        
    counts_data = np.array(df_counts)
    if is_gene_expression:
        #gene_array = np.broadcast_to(df_counts.index.values,df_counts.T.shape).T
        gene_numbers = [int(x[7:]) for x in df_counts.index.values]  # Not general
        # Cast as int, not string for performance reasons
        gene_array = np.outer(gene_numbers, np.ones(df_counts.shape[1])).astype('int')
        df_gene_table = pd.read_csv('three_bears_liver_rnaseq_geneInfo.txt', sep='\t').set_index('gene.id')
        df_gene_table['gene_ids'] = [int(x[7:]) for x in df_gene_table.index.values]
        
        experiment_id = [int(x[5:]) for x in df_counts.columns]
        experiment_array = np.broadcast_to(experiment_id,df_counts.shape).astype('int')
        #np.outer(experiment_id, np.ones(df_counts.shape[1])).astype('int')
        df_metadata['orsam_id'] = [int(x[5:]) for x in df_metadata['barcode']]

    def get_sex_encoding(x,numeric=False):
        sex = df_metadata.loc[x, 'sex']
        male_tags = ['Male', 'male', 'M', 'm']
        female_tags = ['Female', 'female', 'f', 'F']
        if sex in male_tags:
            if numeric:
                return 0
            else:
                return 'Male'
        elif sex in female_tags:
            if numeric:
                return 1
            else:
                return 'Female'
        else:
            raise Exception("Bad tag found in sex metadata")

    def get_diet_encoding(x,numeric=False):
        diet = df_metadata.loc[x, 'diet']
        lean_tags = ['10% fat + fiber']
        fat_tags = ['44% fat + fiber', '44% fat+ fiber']  # Random discrepancy in metadata
        if diet in lean_tags:
            if numeric:
                return 0
            else:
                return 'LeanDiet'
        elif diet in fat_tags:
            if numeric:
                return 1
            else:
                return 'FatDiet'
        else:
            raise Exception("Bad tag found in diet metadata")

    def get_strain_encoding(x,numeric=False):
        strain = df_metadata.loc[x, 'strain']
        b6_tags = ['B6', 'C57BL_6J']
        cast_tags = ['CAST', 'CAST_EiJ']
        nzo_tags = ['NZO', 'NZO_HlLtJ']
        if strain in b6_tags:
            if numeric:
                return 0
            else:
                return 'B6'
        elif strain in cast_tags:
            if numeric:
                return 1
            else:
                return 'CAST'
        elif strain in nzo_tags:
            if numeric:
                return 2
            else:
                return 'NZO'
        else:
            raise Exception("Bad tag found in strain metadata")


    def df_to_data(obj,label=None):
        result = Data(label=label)
        for c in obj.columns:
            result.add_component(obj[c], str(c))
        return result


    data_name = Path(matrix_file).stem[:-14]  # Short name for dataset
    if is_gene_expression:
        return [Data(counts=counts_data, gene_ids=gene_array, exp_ids=experiment_array,
                    label=data_name),
                df_to_data(df_metadata,label='rnaseq_metadata'),
                df_to_data(df_gene_table,label='rnaseq_gene_info')]
               # Data(geneid=df_gene_table.index.values, symbol=df_gene_table['symbol'],
                #     entrez_id=df_gene_table['entrez_id'], chr=df_gene_table['chr'],
                #     start=df_gene_table['start'], end=df_gene_table['end'],
                #     middle=df_gene_table['middle'],
                #     strand=df_gene_table['strand'], gene_ids=df_gene_table['gene_ids'],
                #     label='gene_info_table')]
    elif is_atac:
        return [Data(counts=counts_data, atac_peak_ids=atac_ids_array, exp_ids=experiment_array,
                     label=data_name),
                df_to_data(df_metadata,label='atacseq_metadata'),
                Data(atac_peak_ids=atac_ids,
                     chr=chr,
                     start=starts,
                     end=ends,
                     label='atacseq_peak_info')]
