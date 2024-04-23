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
top_frame.place(x = 0, y = 0)

game_title = Label(
    top_frame,
    bg = 'black',
    fg = 'white',
    text = 'Minesweeper',
    font = ('', 50)
)

game_title.place(
    x = utilities.width_size(35),
    y = 10
)

left_frame = Frame(
   window,
   bg='black',
   width=utilities.width_size(20),
   height=utilities.height_size(100)
    )
left_frame.place(
    x=20,
    y=utilities.height_size(20)
    )

center_frame = Frame(
   window,
   bg='black',
   width=utilities.width_size(100),
   height=utilities.height_size(100)
    )
center_frame.place(
    x=utilities.width_size(25),
    y=utilities.height_size(15)
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
#Cell.show_all_mines()


# Run the window
window.mainloop() #Run until closed
