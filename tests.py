import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    
    def test_maze_win_is_none(self):
        num_cols = 8
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertIsNone(m1._Maze__win)


if __name__ == "__main__":
    unittest.main()