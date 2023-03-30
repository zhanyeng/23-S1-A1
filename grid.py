from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import AdditiveLayerStore, LayerStore, SequenceLayerStore, SetLayerStore


class Grid:
    """"
    This code defines a class called Grid that represents a 2D grid of squares.
    The grid is implemented using a referential array (which is a kind of 2D array).
    """
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

    def __init__(self, draw_style, x: int, y: int) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        """"
        Complexity:O(xy) as it initializes the grid of size xy with LayerStore objects. 
        The for-loops to initialize the grid have nested loops which iterate through the rows and columns of the grid.
        """
        if x < 0 or y < 0:
            raise ValueError("Cannot be negative!")
        self.row = x
        self.col = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE
        self.drawStyle = draw_style

        self.grid = ArrayR(self.row)
        for i in range(self.row):
            self.grid[i] = ArrayR(self.row)
            for j in range(self.col):
                if self.drawStyle == Grid.DRAW_STYLE_ADD:
                    self.grid[i][j] = AdditiveLayerStore()
                elif self.drawStyle == Grid.DRAW_STYLE_SET:
                    self.grid[i][j] = SetLayerStore()
                elif self.drawStyle == Grid.DRAW_STYLE_SEQUENCE:
                    self.grid[i][j] = SequenceLayerStore()

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        """"
        Complexity:O(1)
        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        """"
        Complexity:O(1)
        """
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        """
        Complexity:O(x*y)
        """
        for i in range(self.row):
            for j in range(self.col):
                self.grid[i][j].special()
