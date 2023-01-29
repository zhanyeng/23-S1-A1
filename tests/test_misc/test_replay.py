import unittest
from ed_utils.decorators import number

from action import PaintAction, PaintStep
from replay import ReplayTracker
from layers import green, red
from grid import Grid

class TestReplay(unittest.TestCase):

    @number("5.1")
    def test_basic(self):
        grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)
        control_grid = Grid(Grid.DRAW_STYLE_SET, 10, 10)

        steps1 = [PaintStep((4, 4), green), PaintStep((4, 5), green), PaintStep((5, 4), green)]
        steps2 = [PaintStep((5, 5), red), PaintStep((4, 4), red)]

        replay = ReplayTracker()
        replay.add_action(PaintAction(
            steps1[:],
            False
        ))
        replay.add_action(PaintAction(
            steps2[:],
            False
        ))
        # Do the replay
        replay.start_replay()
        v1 = replay.play_next_action(grid)
        v2 = replay.play_next_action(grid)
        v3 = replay.play_next_action(grid)
        self.assertEqual((v1, v2, v3), (False, False, True), "Wrong value returned from play_next_action")
        # Manually do
        for step in steps1 + steps2:
            step.redo_apply(control_grid)

        self.assertGridEqual(grid, control_grid)

    def assertGridEqual(self, grid1: Grid, grid2: Grid):
        for x in range(len(grid1.grid)):
            for y in range(len(grid1[x])):
                sq1 = grid1[x][y]
                sq2 = grid2[x][y]
                self.assertEqual(
                    sq1.get_color((0, 0, 0), 0, x, y),
                    sq2.get_color((0, 0, 0), 0, x, y),
                    "Grid not the same after apply has been made."
                )

