from tkinter import Tk, ttk, BOTH, Canvas, Entry, StringVar, IntVar, DoubleVar, messagebox, Button
import tkinter as tk
from enum import Enum
from constants import WINDOW_TITLE, WINDOW_COLOR, TRANSPARENT_COLOR

class Window:

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title(WINDOW_TITLE)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, width=width, height=height, bg=WINDOW_COLOR)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while(self.__running):
            self.redraw()
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def draw_label(self, label):
        label.draw(self.__root)
    
    def draw_input(self, input):
        input.draw(self.__root)
    
    def create_button(self, x, y, text, command, bg="#B9B9B9", fg="#000000"):
        button = Button(self.__root, text=text, command=command, bg=bg, fg=fg)
        button.place(x=x,y=y)

    def clear_canvas(self):
        self.__canvas.delete("all")

    def alert(self, msg):
        messagebox.showwarning(message=msg)
    
    def confirm(self, msg):
        return messagebox.askyesno(message=msg)

    def close(self):
        self.__running = False


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)
    
class Label:

    def __init__(self, x, y, text, font_name="Helvetica", font_size="10", font_weight="normal", text_color="black", anchor="n"):
        self.__x = x
        self.__y = y
        self.text = text
        self.__font = (font_name, font_size, font_weight)
        self.__text_color = text_color
        self.__anchor = anchor
        self.obj = None
    
    def draw(self, root):
        self.obj = tk.Label(root, text=self.text, font=self.__font, fg=self.__text_color, anchor=self.__anchor, bg=TRANSPARENT_COLOR)
        self.obj.place(x=self.__x, y=self.__y)

class InputType(Enum):
    TEXT = "text"
    INT = "int"
    DOUBLE = "double"

class Input:

    def __init__(self, name, x, y, width, type=InputType.TEXT, font=("Helvetica", "12", "normal"), label_text=None, label_font=("Helvetica", "12", "normal")):
        self.name = name
        self.__x = x
        self.__y = y
        self.__width = width
        self.__type = type
        self.font = font
        self.__label_text = label_text
        self.__label_font = label_font
        self.obj = None
        self.var = self.createTkVar(self.name, self.__type)

    def draw(self, root):
        self.draw_label(root)
        self.obj = Entry(root, textvariable=self.var, font=self.font)
        self.place()
    
    def draw_label(self, root):
        if self.__label_text is None:
            return
        label = Label(self.__x, self.__y, self.__label_text, font_name=self.__label_font[0], font_size=self.__label_font[1], font_weight=self.__label_font[2], anchor="n")
        label.draw(root)
        root.update() # updating in order to retrieve the correct width of the label
        self.__x += label.obj.winfo_width() + 10
    
    def createTkVar(self, name, type):
        if type == InputType.TEXT:
            return StringVar(name=name)
        if type == InputType.INT:
            return IntVar(name=name)
        if type == InputType.DOUBLE:
            return DoubleVar(name=name)
        
        raise Exception(f"{type} variable not supported")
    
    def place(self):
        self.obj.place(x=self.__x, y=self.__y + 10, width=self.__width, anchor="w")

    def get(self):
        return self.var.get()

class Combobox(Input):

    def __init__(self, name, x, y, width, values, type=InputType.TEXT, font=("Helvetica", "12", "normal"), label_text=None, label_font=("Helvetica", "12", "normal"), state="readonly"):
        if not isinstance(values, list):
            raise Exception("Invalid input for combobox values")
        
        self.__values = values
        self.__state = state

        super().__init__(name, x, y, width, type, font, label_text, label_font)

    def draw(self, root):
        self.draw_label(root)
        self.obj = ttk.Combobox(root, textvariable=self.var, font=self.font, state=self.__state)
        self.obj["values"] = self.__values
        if len(self.__values) > 0:
            self.obj.current(0)
        self.place()
