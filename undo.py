from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack


class UndoTracker:
    """
    This code has a time complexity of O(1) for all methods since they all involve only constant time operations such
    push and pop on a stack. The size of the input (max_size and grid) does not affect the running time of the methods.
    Therefore, the time complexity is constant for all methods.
    """
    """"
    This code implements an UndoTracker class that allows for undo and redo functionality in a paint application. 
    The class uses two stacks, one for undoing and one for redoing, to keep track of PaintActions.
    """

    def __init__(self, max_size: int):
        """
        Initializes an empty undo tracker with the given capacity.
        """
        self.undo_stack = ArrayStack(max_size)
        self.redo_stack = ArrayStack(max_size)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        Return type:None
        """
        if not self.undo_stack.is_full():
            self.undo_stack.push(action)

    def undo(self, grid: Grid) -> PaintAction | None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if not self.undo_stack.is_empty():
            action = self.undo_stack.pop()
            action.undo(grid)
            self.redo_stack.push(action)
            return action
        return None

    def redo(self, grid: Grid) -> PaintAction | None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if not self.redo_stack.is_empty():
            action = self.redo_stack.pop()
            action.redo(grid)
            self.undo_stack.push(action)
            return action
        return None
