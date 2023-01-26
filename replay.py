from __future__ import annotations
from action import PaintAction

class ReplayTracker:


    def start_replay(self):
        pass

    def add_action(self, action: PaintAction, is_undo: bool=False):
        pass

    def play_next_action(self, grid):
        pass
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """
