import os
from ..hic_factory import read_hic

DATA = os.path.join(os.path.dirname(__file__), 'data')


def test_load_sample_hic():
    hic_data = read_hic(os.path.join(DATA, 'test.hic'), chr1='1', chr2='1')
    assert len(hic_data['x']) == 3957