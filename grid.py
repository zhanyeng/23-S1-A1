from __future__ import annotations
from datatypes.referential_array import ArrayR
from layer_util import Layer
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y, layers: ArrayR[Layer]) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
        - x, y: The dimensions of the grid.
        - num_layers: The number of layers that the window has access to.
        """

    def increase_brush_size(self):
        raise NotImplementedError()

    def decrease_brush_size(self):
        raise NotImplementedError()
