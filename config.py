from graphics import Label, Input, InputType, Combobox
from constants import *
from maze import Maze

class Config:

    def __init__(self, win):
        self.__win = win
        self.__num_cols_input = None
        self.__num_rows_input = None
        self.__algo_input = None
        self.__maze = None
        self.__maze_generating = False
    
    def draw_config(self):
        mz_conf_lbl = Label(CONFIG_TITLE_X, CONFIG_TITLE_Y, CONFIG_TITLE_TEXT, font_size=CONFIG_TITLE_FONT_SIZE, font_weight="bold")
        self.__num_cols_input = Input("num_cols", NUM_COLS_INPUT_X, NUM_COLS_INPUT_Y, INPUT_WIDTH, label_text="Columns:", type=InputType.INT)
        self.__algo_input = Combobox("algo", SOLVE_ALGO_INPUT_X, SOLVE_ALGO_INPUT_Y, SOLVE_ALGO_INPUT_WIDTH, SOLVE_ALGOS)
        self.__num_rows_input = Input("num_rows", NUM_ROWS_INPUT_X, NUM_ROWS_INPUT_Y, INPUT_WIDTH, label_text="Rows:", type=InputType.INT)

        self.__win.draw_label(mz_conf_lbl)
        self.__win.draw_input(self.__num_cols_input)
        self.__win.draw_input(self.__num_rows_input)

        self.__win.create_button(LOAD_MAZE_BUTTON_X, LOAD_MAZE_BUTTON_Y, "CREATE MAZE", self.create_maze, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR)

        self.__win.draw_input(self.__algo_input)
        self.__win.create_button(SOLVE_MAZE_BUTTON_X, SOLVE_MAZE_BUTTON_Y, "SOLVE", self.solve_maze, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR)

    
    def create_maze(self):
        generate = True
        if self.__maze is not None:
            generate = False
            if self.__maze.solving:
                generate = self.__win.confirm("The maze is currently getting solved.\nWould you like to stop and generate a new maze?")
                self.__maze.abort_solving()
            if not generate:
                generate = self.__win.confirm("Generating a new maze will delete the current one.\nProceed?")

            if not generate:
                return
            self.__win.clear_canvas()
            self.__maze = None

        if self.__maze_generating:
            if not self.__win.confirm("Generating a new maze will delete the current one.\nProceed?"):
                return
        
        self.__maze_generating = True

        screen_x = SCREEN_X
        screen_y = SCREEN_Y
        margin = MAZE_X1

        num_cols = self.__num_cols_input.get()
        num_rows = self.__num_rows_input.get()

        if num_cols <= 0:            
            self.__win.alert("Number of columns required")
            return

        if num_rows <= 0:            
            self.__win.alert("Number of rows required")
            return

        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows

        self.__maze = Maze(margin, margin * 2 - 10, num_rows, num_cols, cell_size_x, cell_size_y, self.__win, seed="test")

        self.__maze_generating = False
    
    def solve_maze(self):
        if self.__maze is None or not self.__maze.loaded:
            self.__win.alert("Maze not loaded")
            return
        
        if self.__maze.solving:
            self.__win.alert("The maze is already being solved")
            return
        
        if self.__maze.tried_solving:
            if self.__maze.solved:
                self.__win.alert("Maze was already solved")
            else:
                self.__win.alert("Already tried to solve but no path was found")
            return

        self.__maze.solve(self.__algo_input.get())

