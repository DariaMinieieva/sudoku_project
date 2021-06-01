"""
This module is the main module for the crossword
and serves for the crossword solving and drawing.
"""

import random
import tkinter  as tk
import tkinter.font as tkFont
from arrays import Array2D
from crossword_backtracking.backtracking import CrosswordSolver


class CrosswordDrawer:
    """Class for crossword drawing and interaction with user."""

    def __init__(self, crossword_file: str) -> None:
        """Creates a new Crossword Drawer."""
        self.crossword_file = crossword_file
        self.mode = self.choose_mode()
        self.grid = self.read_matrix()
        self.solver = CrosswordSolver(self.grid)
        self.words_num = self.get_words_num()


    def choose_mode(self) -> int:
        """
        Allows a user to choose the mode for crossword solving:
        1st mode is their input of the words, from which a crossword will be built;
        2nd mode is building a crossword from random words from a dictionary.
        """
        mode = input("Choose the mode of crossword solving:\n\
1) from your input words;\n2) from random words from dictionary\n")
        if mode in ('1', '2'):
            mode = int(mode)
        else:
            mode = self.choose_mode()
        return mode


    def read_matrix(self):
        """Returns a 2D Array with the grid for crossword that is read from file."""
        with open(self.crossword_file, encoding='utf-8') as grid_f:
            self.num_row, self.num_col = map(int, grid_f.readline().split())
            grid = Array2D(self.num_row, self.num_col)
            row_pos = 0
            for row in grid_f:
                for col_pos in range(self.num_col):
                    grid[row_pos, col_pos] = row[col_pos]
                row_pos += 1
        return grid


    def get_random(self, file: str) -> list:
        """Returns random words from file."""
        words = []
        with open(file, encoding='utf-8') as words_f:
            for word in words_f:
                words.append(word.strip().upper())
        random.shuffle(words)
        final_words = []
        left = self.words_num
        while left:
            word = words.pop()
            if len(word) > 2:
                final_words.append(word)
                left -= 1
        return final_words


    def get_user_words(self) -> list:
        """Returns list of user words."""
        words = []
        left = self.words_num
        while left:
            print(f'You have {left} words left to enter.')
            word = input("Enter the word to be in the crossword: ")
            if len(word) < 3:
                print("Word must must be not shorter than 3 symbols.")
            elif word.upper() in words:
                print("Ypu have already entered this word.")
            else:
                words.append(word.upper())
                left -= 1
        return words


    def get_words_num(self) -> int:
        """Returns the number of words that can be placed into the grid."""
        words_num = len(self.solver.place_possible())
        return words_num


    def get_final_grid(self):
        """Returns the grid after placing the words into it."""
        if self.mode == 1:
            words = self.get_user_words()
        else:
            words = self.get_random('words.txt')
        self.solver.set_words(words)
        self.solver.place_words()
        return len(self.solver.matrix_results)


    def draw_matrix(self, matrix, num_option: int, options: int):
        """Draws one matrix with Tkinter."""
        root = tk.Tk()
        root.title(f"Option #{num_option}/{options}")
        root.geometry(f"{34*self.num_row}x{36*self.num_col}")
        font_style = tkFont.Font(family="Lucida Grande", size=20)
        for i in range(self.num_col):
            for j in range(self.num_row):
                if matrix[i, j] == '+':
                    color = 'black'
                    matrix[i, j] = ''
                else:
                    color = 'white'
                if matrix[i, j] == '-':
                    matrix[i, j] = ''
                entry = tk.Text(root, height=1, width=2, fg='black', bg=color, font=font_style)
                entry.grid(row=i, column=j)
                entry.insert(tk.END, matrix[i, j])
        root.mainloop()


    def visualize_crossword(self):
        """Visualizes the crossword, its possible solvings."""
        options = self.get_final_grid()
        if options == 0:
            self.draw_matrix(self.grid, 0, options)
        else:
            for i, item in enumerate(self.solver.matrix_results):
                self.draw_matrix(item.matrix, i+1, options)


if __name__ == "__main__":
    try:
        a = CrosswordDrawer('grid1.txt')
        a.visualize_crossword()
    except (AssertionError, IndexError, TypeError):
        print('Wrong index input in crossword file')
