def setup():
    from .bed_factory import read_bed  # noqa
    from .bedgraph_factory import read_bedgraph  # noqa
    from .bigwig_factory import read_bigwig  # noqa
    from .matrix_factory import read_matrix # noqa
    from .bedpe_factory import read_bedpe # noqa
    from .peak_correlations_factory import read_peak_correlations

    from .viewers.network.data_viewer import NetworkDataViewer # noqa
