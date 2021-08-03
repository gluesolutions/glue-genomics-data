from glue.viewers.common.state import ViewerState
from echo import CallbackProperty, SelectionCallbackProperty
from glue.core.data_combo_helper import ComponentIDComboHelper


class NetworkViewerState(ViewerState):
    x_att = SelectionCallbackProperty(docstring='The attribute to use on the x-axis')
    y_att = SelectionCallbackProperty(docstring='The attribute to use on the y-axis')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._x_att_helper = ComponentIDComboHelper(self, 'x_att')
        self._y_att_helper = ComponentIDComboHelper(self, 'y_att')
        self.add_callback('layers', self._on_layers_change)

    def _on_layers_change(self, value):
        # self.layers_data is a shortcut for
        # [layer_state.layer for layer_state in self.layers]
        self._x_att_helper.set_multiple_data(self.layers_data)
        self._y_att_helper.set_multiple_data(self.layers_data)
