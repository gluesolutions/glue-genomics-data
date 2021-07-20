from glue.config import data_factory
from glue.core import Data
from astropy.table import Table
from pathlib import Path


__all__ = ['is_bedgraph', 'read_bedgraph']


def is_bedgraph(filename, **kwargs):
    return filename.endswith('.bedgraph')


@data_factory('BedGraph data loader', is_bedgraph)
def read_bedgraph(file_name):
    """
    Read a bedgraph file into glue. 

    Notes
    -----
    Similar to the bigwig files, this is quite slow with large data. Can look
    into using the pyBedGraph package to parse a selection of the file, but
    this would require allowing to load a second chromosome lookup table.
    """
    bg_data = Table.read(file_name, format='ascii.no_header')

    # It seems to be standard that the first three column names are fixed
    bg_data.rename_columns(('col1', 'col2', 'col3', 'col4'), 
                           ('Chromosome', 'Start', 'End', 'Value'))

    return Data(**{k: bg_data[k] for k in bg_data.colnames}, 
                label=Path(file_name).stem)