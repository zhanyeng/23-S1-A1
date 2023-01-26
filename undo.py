from __future__ import annotations
from action import PaintAction
from grid import Grid

class UndoTracker:

    def add_action(self, action: PaintAction):
        pass
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """

    def undo(self, grid: Grid):
        pass
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        """

    def redo(self, grid: Grid):
        pass
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.
        """
