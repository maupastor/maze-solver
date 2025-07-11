from graphics import Line, Point

class Cell:

    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = win
        self.visited = False

        self.f = float("inf")
        self.g = float("inf")
        self.h = 0
        self.parent_i = 0
        self.parent_j = 0
    
    def draw(self, x1, y1, x2, y2):
        if self.__win is None:
            return

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, fill_color="white")
        
        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_right_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, fill_color="white")
        
        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, fill_color="white")
        
        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self.__win.draw_line(line)
        else:
            self.__win.draw_line(line, fill_color="white")
    
    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        
        x1 = (self.__x1 + self.__x2) // 2
        y1 = (self.__y1 + self.__y2) // 2
        x2 = (to_cell.__x1 + to_cell.__x2) // 2
        y2 = (to_cell.__y1 + to_cell.__y2) // 2

        line = Line(Point(x1, y1), Point(x2, y2))
        if self.__win is not None:
            self.__win.draw_line(line, color)

    def __repr__(self):
        s = ""
        s += f"Top = {self.has_top_wall}, "
        s += f"Right = {self.has_right_wall}, "
        s += f"Bottom = {self.has_bottom_wall}, "
        s += f"Left = {self.has_left_wall}"
        return s
