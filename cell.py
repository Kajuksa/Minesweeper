import tkinter as tk
from tkinter import Button, Label
import settings
import random
import ctypes


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    with open("game_info.txt", "r") as file:
        data = file.readlines()
        wins, loses = map(int, (data[0].split(":")[1].strip(), data[1].split(":")[1].strip()))

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Pridėti objektą į sąrašą
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

    @staticmethod  # naudoti ne kiekvienam cellui o visai klasei vieną kartą
    def create_cell_count_label(location):
        label = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 35)
        )
        Cell.cell_count_label_object = label

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
        # Laimėjimas
        if Cell.cell_count == settings.MINES:
            ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Win, win, win!', 0)
            Cell.wins += 1
            Cell.write_game_info()
            self.reset_game()
        # cancel left click if cell is opened
        self.cell_btn_object.unbind('<button-1')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property  # The @property is a built-in decorator for the property() function in Python. It is used to give "special" functionality to certain methods to make them act as getters, setters, or deleters when we define properties in a class
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
            # print(self.surrounding_cells_mines_length) # tikrinu ar veikia surroundinf_cells_mines_lenght
            self.cell_btn_object.configure(text=self.surrounding_cells_mines_length)
            # Skaiciuoja kiek liko ejimu
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # Jei pasirinkau kaip mine_candidate bet nusprendziau paspaust kad convertintu i systemos spalva
            self.cell_btn_object.configure(bg='SystemButtonFace')
        # Pazymiu kad langelis yra atidarytas
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
        )  # sample yra metodas kuris paziuri pirma i lista ir td kiek bombu mum reik
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

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    @staticmethod
    def write_game_info():
        filename = "game_info.txt"
        with open(filename, "w") as file: 
            record = f"Wins: {Cell.wins}\nLoses: {Cell.loses}" 
            file.write(record)
            file.write(record)

