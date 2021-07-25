import os
from ..bedpe_factory import read_bedpe

DATA = os.path.join(os.path.dirname(__file__), 'data')

def test_load_sample_bedpe():
    bedpe_data = read_bedpe(os.path.join(DATA, 'test.bedpe'))
    assert len(bedpe_data['chr_a']) == len(bedpe_data['chr_b'])