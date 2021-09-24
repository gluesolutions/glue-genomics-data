from glue.config import data_factory
from glue.core import Data
import pandas as pd
from pathlib import Path

from glue_genomics_viewers.data import BedPeData

__all__ = ['is_bedpe', 'read_bedpe']


def is_bedpe(filename, **kwargs):
    return filename.endswith('.bedpe')


@data_factory('BEDPE data loader', is_bedpe, priority=999)
def read_bedpe(file_name):
    """
    Read a bed paired-end file denoting linkages between regions
    
    Most of the time these are large datasets we want to display
    on the GenomeTrackViewer and so we load them as the custom
    BedPeData type that knows how to handled tiled/multi-resolution
    data. Although alternatively we could view them as simple 
    datasets that we might want to filter by strength.
    
    """
    
    data = BedPeData(file_name)
    data.engine.index() #This returns quickly if file is already indexed
    return data