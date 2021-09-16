from echo import CallbackProperty, SelectionCallbackProperty
from glue.core.data_combo_helper import ComponentIDComboHelper
from glue.viewers.common.state import LayerState, ViewerState


class NetworkLayerState(LayerState):
    fill = CallbackProperty(False, docstring='Whether to show the markers as filled or not')


class NetworkViewerState(ViewerState):
    layout = SelectionCallbackProperty(
        choices=['Spring', 'Circular', 'Kamada Kawaii', 'Shell'], 
        docstring="Render layout for node graph.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._layout_helper = ComponentIDComboHelper(self, 'layout')
        self.add_callback('layout', self._on_layout_changed)
        # self.add_callback('layers', self._on_layers_change)

    def _on_layers_change(self, value):
        # self.layers_data is a shortcut for
        # [layer_state.layer for layer_state in self.layers]
        # self._x_att_helper.set_multiple_data(self.layers_data)
        # self._y_att_helper.set_multiple_data(self.layers_data)
        pass

    def _on_layout_changed(self, value):
        pass
