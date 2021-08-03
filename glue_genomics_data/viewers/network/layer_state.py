from glue.viewers.common.state import LayerState
from echo import CallbackProperty


class NetworkLayerState(LayerState):
    fill = CallbackProperty(False, docstring='Whether to show the markers as filled or not')