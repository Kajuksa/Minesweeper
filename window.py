from tkinter import * #biblioteka 2d board'ui
from cell import Cell
import settings
import utilities
window = Tk() #Creating a window

# Override the settings of the window
window.configure(bg="black") #spalva
window.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') #dydis
window.title("Minesweeper game") #Pavadinimas
window.resizable(False, False) #nekeiciamas dydis

# Sukuriami langai musu pagrindiniame lange

top_frame = Frame(
   window,
   bg='black',
   width=utilities.width_size(100),
   height=utilities.height_size(20)
    )
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg = 'black',
    fg = 'white',
    text = 'Minesweeper',
    font = ('', 48)
)

game_title.place(
    x = utilities.width_size(25),
    y = 0
)

left_frame = Frame(
   window,
   bg='black',
   width=utilities.width_size(20),
   height=utilities.height_size(100)
    )
left_frame.place(
    x=0,
    y=utilities.height_size(20)
    )

center_frame = Frame(
   window,
   bg='black',
   width=utilities.width_size(80),
   height=utilities.height_size(80)
    )
center_frame.place(
    x=utilities.width_size(30),
    y=utilities.height_size(30)
    )

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column = x, row = y
        )

Cell.random_mines()
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)


# Run the window
window.mainloop() #Run until closed