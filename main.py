from graphics import Window, Line, Point

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(100,100), Point(200, 200)), "green")
    win.draw_line(Line(Point(100,10), Point(300, 10)), "blue")
    win.draw_line(Line(Point(200,200), Point(300, 200)), "red")
    win.draw_line(Line(Point(30,300), Point(300, 300)), "black")
    win.draw_line(Line(Point(500,400), Point(60, 450)), "yellow")
    win.draw_line(Line(Point(180,200), Point(180, 500)), "#CBCBCB")
    win.wait_for_close()

main()