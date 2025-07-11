from cell import Cell
import time
import random

class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        if num_cols > 0 and num_rows > 0:
            self.__break_walls_r(0, 0)
        
        self.__reset_cells_visited()
    
    def __create_cells(self):
        for i in range(self.__num_cols):
            self.__cells.append([])
            for j in range(self.__num_rows):
                self.__cells[i].append(Cell(self.__win))
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)


    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y

        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate(0.01)
    
    def __animate(self, ms=0.05):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(ms)
    
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)
    
    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            directions = []
            if i > 0 and self.__cells[i - 1][j].visited == False:
                directions.append([i - 1, j])
            if i < self.__num_cols - 1 and self.__cells[i + 1][j].visited == False:
                directions.append([i + 1, j])
            if j > 0 and self.__cells[i][j - 1].visited == False:
                directions.append([i, j - 1])
            if j < self.__num_rows - 1 and self.__cells[i][j + 1].visited == False:
                directions.append([i, j + 1])
            
            if len(directions) == 0:
                self.__draw_cell(i, j)
                return

            cell_to_break_idx = random.randrange(len(directions))
            cell_to_break = directions[cell_to_break_idx]
            directions.pop(cell_to_break_idx)

            if i - 1 == cell_to_break[0] and j == cell_to_break[1]:
                self.__cells[i][j].has_left_wall = False
                self.__cells[cell_to_break[0]][cell_to_break[1]].has_right_wall = False
            if i + 1 == cell_to_break[0] and j == cell_to_break[1]:
                self.__cells[i][j].has_right_wall = False
                self.__cells[cell_to_break[0]][cell_to_break[1]].has_left_wall = False
            if i == cell_to_break[0] and j - 1 == cell_to_break[1]:
                self.__cells[i][j].has_top_wall = False
                self.__cells[cell_to_break[0]][cell_to_break[1]].has_bottom_wall = False
            if i == cell_to_break[0] and j + 1 == cell_to_break[1]:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[cell_to_break[0]][cell_to_break[1]].has_top_wall = False
            
            self.__draw_cell(*cell_to_break)

            self.__break_walls_r(*cell_to_break)

    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False
    
    def solve(self):
        return self.solve_r(0, 0)
    
    def solve_r(self, i, j):
        self.__animate(0.03)
        cell = self.__cells[i][j]
        cell.visited = True

        if i + 1 == self.__num_cols and j + 1 == self.__num_rows:
            return True

        next_cells = []
        if i > 0 and not cell.has_left_wall and self.__cells[i - 1][j].visited == False:
            next_cells.append([i - 1, j])
        if i < self.__num_cols - 1 and not cell.has_right_wall and self.__cells[i + 1][j].visited == False:
            next_cells.append([i + 1, j])
        if j > 0 and not cell.has_top_wall and self.__cells[i][j - 1].visited == False:
            next_cells.append([i, j - 1])
        if j < self.__num_rows - 1 and not cell.has_bottom_wall and self.__cells[i][j + 1].visited == False:
            next_cells.append([i, j + 1])
        
        for next in next_cells:
            next_cell = self.__cells[next[0]][next[1]]
            cell.draw_move(next_cell)
            if self.solve_r(*next):
                return True
            cell.draw_move(next_cell, undo=True)
            self.__animate(0.20)
        
        return False
    
    def solve_a_star(self, start, goal):
        open_list = []

        self.__cells[start[0]][start[1]].f = 0
        self.__cells[start[0]][start[1]].g = 0
        self.__cells[start[0]][start[1]].h = 0
        self.__cells[start[0]][start[1]].parent_i = start[0]
        self.__cells[start[0]][start[1]].parent_j = start[1]

        open_list.append([(start[0], start[1]), 0])

        while len(open_list) > 0:
            qi = self.find_lowest_score_element(open_list)
            q = open_list.pop(qi)

            i = q[0][0]
            j = q[0][1]
            self.__cells[i][j].visited = True

            directions = []
            if i > 0 and not self.__cells[i][j].has_left_wall and self.__cells[i - 1][j].visited == False:
                directions.append([i - 1, j])
            if i < self.__num_cols - 1 and not self.__cells[i][j].has_right_wall and self.__cells[i + 1][j].visited == False:
                directions.append([i + 1, j])
            if j > 0 and not self.__cells[i][j].has_top_wall and self.__cells[i][j - 1].visited == False:
                directions.append([i, j - 1])
            if j < self.__num_rows - 1 and not self.__cells[i][j].has_bottom_wall and self.__cells[i][j + 1].visited == False:
                directions.append([i, j + 1])
            
            for dir in directions:
                new_i = dir[0]
                new_j = dir[1]

                if new_i == goal[0] and new_j == goal[1]:
                    # goal reached
                    self.__cells[new_i][new_j].parent_i = i
                    self.__cells[new_i][new_j].parent_j = j
                    self.trace_path(self.__cells, goal)
                    return True
                else:
                    g_new = self.__cells[i][j].g + 1
                    h_new = self.calculate_h_a_star(new_i, new_j, goal)
                    f_new = g_new + h_new

                    if self.__cells[new_i][new_j].f == float("inf") or f_new <= self.__cells[new_i][new_j].f:
                        open_list.append([(new_i, new_j), f_new])
                        self.__cells[new_i][new_j].f = f_new
                        self.__cells[new_i][new_j].g = g_new
                        self.__cells[new_i][new_j].h = h_new
                        self.__cells[new_i][new_j].parent_i = i
                        self.__cells[new_i][new_j].parent_j = j
        
        return False

    def calculate_h_a_star(self, i, j, goal):
        # Euclidean distance
        return ((i - goal[0]) ** 2 + (j - goal[1]) ** 2) ** 0.5

    def trace_path(self, cell_details, dest):
        print("The Path is ")
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        self.draw_path_a_star(path)

    def draw_path_a_star(self, path):
        cell = None
        for coords in path:
            self.__animate()
            next_cell = self.__cells[coords[0]][coords[1]]
            if cell is not None:
                cell.draw_move(next_cell)
            cell = next_cell

    
    def find_lowest_score_element(self, l):
        if l is None or not isinstance(l, list):
            return None
        
        min_index = None
        current_min_score = float("inf")
        for i in range(len(l)):
            cell_x = l[i][0][0]
            cell_y = l[i][0][1]
            if self.__cells[cell_x][cell_y].f != float("inf") and self.__cells[cell_x][cell_y].f < current_min_score:
                min_index = i
                current_min_score = self.__cells[cell_x][cell_y].f
        
        return min_index

    def __repr__(self):
        s = ""
        for i in range(self.__num_cols):
            s += f"\n|"
            for j in range(self.__num_rows):
                cell = self.__cells[i][j]
                s += f" Cell [{i}, {j}]: {str(cell)} |"
        return s

