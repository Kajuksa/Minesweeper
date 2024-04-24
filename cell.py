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
