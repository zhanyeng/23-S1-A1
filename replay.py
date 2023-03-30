from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class ReplayTracker:
    def __init__(self,max_capacity:int):
        """"
        __init__(self, max_capacity:int): This initializes the object with an ArrayStack for actions and undo_actions.
        The maximum capacity of the stack is passed as an argument.
        """
        """"
        Complexity:O(1)
        """
        self.actions = ArrayStack(max_capacity)
        self.undo_actions = ArrayStack(max_capacity)
        self.playback = False

    def __init__(self):
        """"
        There is a second __init__ method defined which does not take any arguments and
        initializes the actions and undo_actions stacks with a default maximum capacity of 10.
        """
        """"
        Complexity:O(1)
        """
        self.actions = ArrayStack(10)
        self.undo_actions = ArrayStack(10)
        self.playback = False


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        """"
        Complexity:O(1)
        Return type:None
        """
        self.playback = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        """"
        Complexity:O(1) (assuming the underlying ArrayStack has O(1) push operations)
        Return type:None
        """
        if not self.playback:
            self.actions.push(action)
            if is_undo:
                self.undo_actions.push(action)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """
        """"
        Complexity: O(k), where k is the number of steps in the next PaintAction object that is popped from the actions stack. 
        This is because the method applies each PaintStep object in the PaintAction object to the corresponding grid squares
        in a loop. The maximum value of k is bounded by the size of the grid, so this method can be considered to have a 
        worst-case time complexity of O(n^2), where n is the size of the grid.
        Return type: Boolean
        """

        if len(self.actions) == 0:
            return True
        action = self.actions.pop()
        for step in action.steps:
            row, col = step.affected_grid_square
            step.redo_apply(grid[row][col])
        return False

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

