from glue.config import data_factory
from glue.core import Data
from astropy.table import Table
from pathlib import Path

from glue_genomics_viewers.data import BedgraphData


__all__ = ['is_bedgraph', 'read_bedgraph']


def is_bedgraph(filename, **kwargs):
    return filename.endswith('.bedgraph')


@data_factory('BedGraph data loader', is_bedgraph, priority=999)
def read_bedgraph(file_name):
    """
    Read a bedgraph file into glue. 

    Most of the time these are large datasets we want to display
    on the GenomeTrackViewer and so we load them as the custom
    BedgraphData type that knows how to handled tiled/multi-resolution
    data. Although alternatively we could view them as simple 
    datasets that we might want to filter by strength.
    """
    data = BedgraphData(file_name)
    data.engine.index() #This returns quickly if file is already indexed
    return data