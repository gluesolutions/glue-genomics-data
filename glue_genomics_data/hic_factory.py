from glue.config import data_factory
from glue.core import Data
import strawC
import numpy as np


def is_hic(filename, **kwargs):
    return filename.endswith('.hic')


@data_factory(label='Hi-C data laoder', identifier=is_hic)
def read_hic(filename):
    """Read a HiC file into glue

    Need a custom UI or something to specify parameters
    This just hard-codes some sensible defaults.
    """
    hic_data = strawC.strawC("observed", "NONE", filename, "3", "3", "BP", 50000)

    def extract(x):
        return(x.binX, x.binY, x.counts)
    converted_data = np.array(list(map(extract, hic_data)), dtype=np.int64)
    data = Data(x=converted_data[:,0]//10000,
                y=converted_data[:,1]//10000,
                counts=converted_data[:,2])
    return data