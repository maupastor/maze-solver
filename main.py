from graphics import Window, Label, Input, InputType
from config import Config
from constants import SCREEN_X, SCREEN_Y
from maze import Maze

def main():
    num_rows = 8
    num_cols = 6
    margin = 50

    screen_x = SCREEN_X
    screen_y = SCREEN_Y

    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    win = Window(screen_x, screen_y)
    config = Config(win)
    config.draw_config()

    win.wait_for_close()
    

main()