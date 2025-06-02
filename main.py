from graphics import Window
from cell import Cell

def main():
    win = Window(800, 600)
    cell1 = Cell(win)
    cell1.has_right_wall = False
    cell1.draw(100, 150, 150, 200)

    cell2 = Cell(win)
    cell2.has_left_wall = False
    cell2.has_bottom_wall = False
    cell2.draw(150, 150, 200, 200)

    cell3 = Cell(win)
    cell3.has_top_wall = False
    cell3.draw(150, 200, 200, 250)

    cell1.draw_move(cell2)
    cell2.draw_move(cell3, True)

    win.wait_for_close()
    

main()