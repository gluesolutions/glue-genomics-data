from glue.config import data_factory
from glue.core import Data
import strawC
from straw import straw_module
import numpy as np


__all__ = ['is_hic', 'read_hic']


def is_hic(filename, **kwargs):
    try:
        _ = straw_module.read_metadata(filename, verbose=0)
    except NameError:  # straw module throws this (incorrect) error with malformed .hic
        return False
    return True


@data_factory(label='Hi-C data loader', identifier=is_hic)
def read_hic(filename, chr1='1', chr2='1', resolution=None):
    """Read a HiC file into glue

    Need a custom UI or something to specify parameters
    This just hard-codes some sensible defaults for the
    test dataset (chr3 and other parameters for ChIA-PET)
    """
    metadata = straw_module.read_metadata(filename, verbose=0)
    max_resolution = metadata['Base pair-delimited resolutions'][0]  # This is true for sample data. Is it always true?
    if not resolution:
        resolution = metadata['Base pair-delimited resolutions'][-1]  # This is true for sample data. Is it always true?

    hic_data = strawC.strawC("observed", "NONE", filename, chr1, chr2, "BP", resolution)  # Min resolution, all chromosomes

    def extract(x):
        return(x.binX, x.binY, x.counts)
    converted_data = np.array(list(map(extract, hic_data)), dtype=np.int64)
    data = Data(chr1=converted_data[:,0]//10000,
                chr2=converted_data[:,1]//10000,
                counts=converted_data[:,2])
    return data