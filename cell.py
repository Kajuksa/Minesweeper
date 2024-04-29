import tkinter as tk
from tkinter import Button, Label
import settings
import random
import ctypes

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    @classmethod
    def initialize(cls):
        with open("game_info.txt", "r") as file:
            data = file.readlines()
            cls.wins, cls.loses = map(int, (data[0].split(":")[1].strip(), data[1].split(":")[1].strip()))

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4
        )
        btn.bind('<Button-1>', self.left_click)
        btn.bind('<Button-3>', self.right_click)
        self.cell_btn_object = btn

    @classmethod
    def create_cell_count_label(cls, location):
        cls.cell_count_label_object = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{cls.cell_count}",
            font=("", 35)
        )

    def left_click(self, event):
        if self.is_mine:
            self.show_mine()
            Cell.loses += 1
            Cell.write_game_info()
        else:
            if self.surrounding_cells_mines_length == 0:
                for cell_obj in self.surrounding:
                    cell_obj.show_cell()
            self.show_cell()
        if Cell.cell_count == settings.MINES:
            ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Win, win, win!', 0)
            Cell.wins += 1
            Cell.write_game_info()
            self.reset_game()
        self.cell_btn_object.unbind('<Button-1>')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounding(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounding_cells_mines_length(self):
        counter = 0
        for cell in self.surrounding:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounding_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")
            self.cell_btn_object.configure(bg='SystemButtonFace')
        self.is_opened = True

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        self.reset_game()

    def right_click(self, event):
        if not self.is_opened:
            if not self.is_mine_candidate:
                self.cell_btn_object.configure(bg='grey')
            else:
                self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_mine_candidate = not self.is_mine_candidate

    @staticmethod
    def random_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    @staticmethod
    def show_all_mines():
        for cell in Cell.all:
            if cell.is_mine:
                cell.cell_btn_object.configure(bg='yellow')

    @staticmethod
    def reset_game():
        for cell in Cell.all:
            cell.is_opened = False
            cell.is_mine = False
            cell.is_mine_candidate = False
            cell.cell_btn_object.configure(bg='SystemButtonFace')
            cell.cell_btn_object.configure(text='')
        Cell.cell_count = settings.CELL_COUNT
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")
        Cell.random_mines()
        Cell.write_game_info()

    @staticmethod
    def write_game_info():
        filename = "game_info.txt"
        with open(filename, "w") as file: 
            record = f"Wins: {Cell.wins}\nLoses: {Cell.loses}" 
            file.write(record)
            file.write(record)

Cell.initialize()

#Polimorfizmas:
#Method Overriding: Both show_cell() and show_mine() methods are defined in the Cell class. These methods override the behavior of the same-named methods defined in the superclass (in this case, there's no explicit superclass, but conceptually it's the same). When an instance of Cell is created, depending on whether it's a mine or not, calling show_cell() or show_mine() will execute the specific behavior defined in the subclass.
#Common Interface: Despite show_cell() and show_mine() having different implementations, they share a common interface. This means that both methods can be called on any Cell object, and the appropriate behavior (either showing the cell or revealing a mine) will be executed based on the type of Cell object.

#Abstrakcija:
#Class Structure: I have created a Cell class to represent individual cells in a game grid. This class abstracts away the details of each cell's behavior and properties. Users interacting with the game don't need to know how each cell is implemented internally; they only need to know how to interact with it through its methods.
#Method Abstraction: Each method in the Cell class encapsulates a specific behavior or action related to a cell. For example, show_cell() and show_mine() abstract away the details of how a cell is displayed when it's opened or when it contains a mine. Users of the Cell class don't need to know how these methods are implemented internally; they only need to know what they do and how to call them.
#Property Abstraction: I have used properties like surrounding and surrounding_cells_mines_length to abstract away the details of how a cell interacts with its neighboring cells and how it calculates the number of surrounding mines. Users of the Cell class can access these properties without needing to know the exact implementation details.
#Static Methods: You've used static methods like random_mines() and reset_game() to encapsulate certain behaviors that are related to the Cell class but don't depend on the state of individual cell objects. These methods provide abstraction by hiding the implementation details of how mines are randomly placed or how the game is reset.

#Inheritance:
#Kiekvienas sukurtas langelis paveldi iš Cell klasės. Trumpai tariant, viena klasė atsakinga už visus sukurtus langelius, kurie yra sukuriami žaidime.

#Encapsulation:
#Class Definition: MY Cell class encapsulates the attributes and methods related to a single cell in your game grid. All the behavior and properties related to a cell are contained within this class.
#Private Attributes: Although my code doesn't explicitly define private attributes (attributes with names starting with _), the attributes such as is_mine, is_opened, and is_mine_candidate are effectively encapsulated within the Cell class. These attributes are not directly accessible from outside the class and can only be accessed or modified through the class methods.
#Methods as Interface: The methods defined within the Cell class, such as create_btn_object(), left_click(), right_click(), show_cell(), show_mine(), and others, serve as the interface through which external code interacts with the Cell objects. This encapsulates the behavior associated with a cell and hides the implementation details from the outside world.
#Data Integrity: By encapsulating the attributes and providing controlled access through methods, your code ensures data integrity and prevents external code from directly modifying the internal state of a cell in an unintended manner.

#Design patterns:
#Separation of Concerns (SoC): My code separates different concerns into distinct methods and classes. For example, the Cell class encapsulates the behavior and properties related to individual cells, while methods like random_mines() and reset_game() handle game-level functionalities. This promotes modularity and maintainability.
#Single Responsibility Principle (SRP): Each class and method in my code has a single responsibility. For example, the Cell class is responsible for managing the behavior of individual cells, while methods like random_mines() and reset_game() have the responsibility of initializing the game state. This improves code clarity and makes it easier to understand and maintain.
#Observer Pattern (Implicit): Although not explicitly implemented, the event handling mechanism in my code, such as left-click and right-click events on cells, can be seen as an implicit use of the Observer pattern. The cell objects (subject) notify the game logic (observer) when certain events occur, such as a left-click or right-click action.
#Template Method Pattern (Potential): Your code structure suggests the potential for implementing the Template Method pattern. For example, the left_click() and right_click() methods in the Cell class provide a basic algorithmic structure for handling left-click and right-click actions on cells. Subclasses could potentially override these methods to customize the behavior for specific types of cells.
#Factory Method Pattern (Implicit): While not explicitly implemented, the create_btn_object() method in the Cell class can be seen as an implicit use of the Factory Method pattern. It encapsulates the creation of button objects, providing a centralized place for creating instances of buttons associated with cells

