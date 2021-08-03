from glue.viewers.common.layer_artist import LayerArtist
from .layer_state import NetworkLayerState


class NetworkLayerArtist(LayerArtist):

    _layer_artist_cls = NetworkLayerState

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state.add_callback('fill', self._on_fill_change)

    def _on_fill_change(self):

    # Make adjustments to the visualization layer here

    def clear(self):
        pass

    def remove(self):
        pass

    def redraw(self):
        pass

    def update(self):
        pass