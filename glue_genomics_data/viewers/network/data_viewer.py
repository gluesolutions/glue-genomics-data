from glue.viewers.common.viewer import Viewer
from .viewer_state import NetworkViewerState
from .layer_artist import NetworkLayerArtist
from .layer_state import NetworkLayerState


class NetworkDataViewer(Viewer):

    LABEL = 'Tutorial viewer'
    _state_cls = NetworkViewerState
    _data_artist_cls = NetworkLayerArtist
    _subset_artist_cls = NetworkLayerState

    def get_layer_artist(self, cls, layer=None, layer_state=None):
        return cls(self.axes, self.state, layer=layer, layer_state=layer_state)
