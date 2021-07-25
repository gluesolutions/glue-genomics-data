from glue.config import data_factory
from glue.core import Data
import pandas as pd
from pathlib import Path


__all__ = ['is_bedpe', 'read_bedpe']


def is_bedpe(filename, **kwargs):
    return filename.endswith('.bedpe')


@data_factory('BEDPE data loader', is_bedpe)
def read_bedpe(file_name):
    """
    Read a bed paired-end file denoting linkages between regions
    """
    bedpe_data = pd.read_csv(file_name, sep='\t', names=['chr_a',
                                                         'start_a',
                                                         'end_a',
                                                         'chr_b',
                                                         'start_b',
                                                         'end_b',
                                                         'strength'])

    return Data(**{k: bedpe_data[k] for k in bedpe_data.columns},
                label=Path(file_name).stem)
