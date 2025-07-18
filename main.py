from graphics import Window
from maze import Maze

def main():
    num_rows = 8
    num_cols = 6
    margin = 50

    screen_x = 800
    screen_y = 600

    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    win = Window(screen_x, screen_y)
    
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed="test")

    # maze.solve()

    #maze.solve_a_star([0, 0], [num_cols - 1, num_rows - 1])

    maze.solve_bfs([0, 0], [num_cols - 1, num_rows - 1])

    win.wait_for_close()
    

main()