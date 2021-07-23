def setup():
    from .hic_factory import read_hic  # noqa
    from .bed_factory import read_bed  # noqa
    from .bedgraph_factory import read_bedgraph  # noqa
    from .bigwig_factory import read_bigwig  # noqa
    from .matrix_factory import read_matrix