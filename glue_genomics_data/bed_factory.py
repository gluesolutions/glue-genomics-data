from glue.config import data_factory
from glue.core import Data
import pyranges as pr
from pathlib import Path


__all__ = ['is_bed', 'read_bed']


def is_bed(filename, **kwargs):
    return filename.endswith('.bed')


@data_factory('BED data loader', is_bed)
def read_bed(file_name):
    """
    Read a bed file into glue.
    """
    bed_data = pr.read_bed(file_name, as_df=True)

    return Data(**{k: bed_data[k] for k in bed_data.columns}, 
                label=Path(file_name).stem)