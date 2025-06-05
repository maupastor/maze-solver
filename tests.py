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
    
    def test_maze_break_entrance_and_exit(self):
        num_cols = 8
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(
            m1._Maze__cells[0][0].has_top_wall,
            False,
        )

        self.assertEqual(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )
    
    def test_maze_break_walls_r(self):
        num_cols = 3
        num_rows = 4
        seed = "test"

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=seed)
        expected_cells = []

        # top, right, bottom, left
        expected_cells.append([
            [False, True, False, True],
            [False, False, True, True],
            [True, True, False, True],
            [False, False, True, True],
        ])
        expected_cells.append([
            [True, False, True, True],
            [True, False, True, False],
            [True, False, False, True],
            [False, False, True, False],
        ])
        expected_cells.append([
            [True, True, False, False],
            [False, True, False, False],
            [False, True, True, False],
            [True, True, False, False],
        ])

        for i in range(len(expected_cells)):
            for j in range(len(expected_cells[i])):
                exp_cell = expected_cells[i][j]
                actual_cell = m1._Maze__cells[i][j]
                self.assertEqual(exp_cell[0], actual_cell.has_top_wall)
                self.assertEqual(exp_cell[1], actual_cell.has_right_wall)
                self.assertEqual(exp_cell[2], actual_cell.has_bottom_wall)
                self.assertEqual(exp_cell[3], actual_cell.has_left_wall)
        
    def test_maze_reset_cell_visited(self):
        num_cols = 3
        num_rows = 4
        seed = "test"

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=seed)

        visited = False
        for row in m1._Maze__cells:
            for cell in row:
                if cell.visited:
                    visited = True
                    break
            if visited:
                break
        
        self.assertEqual(visited, False)
    
    def test_maze_solve(self):
        num_cols = 6
        num_rows = 8

        margin = 50
        screen_x = 800
        screen_y = 600

        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows

        m1 = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, seed="test")

        solved = m1.solve()
        self.assertEqual(solved, True)


if __name__ == "__main__":
    unittest.main()