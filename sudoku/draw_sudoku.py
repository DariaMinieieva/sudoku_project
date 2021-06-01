"""This module visualizes the solved sudoku."""

from copy import deepcopy
import tkinter as tk
import tkinter.font as tkFont
from board import Board


class SudokuDrawer:
    """Class for solving sudoku and visualizing it."""

    def __init__(self, board: list) -> None:
        """Creates a new sudoku drawer."""
        self.board = deepcopy(board)
        self.sudoku = Board(board)


    def draw_matrix(self, matrix):
        """Draws one matrix with Tkinter."""
        root = tk.Tk()
        root.geometry("500x500")
        font_style = tkFont.Font(family="Lucida Grande", size=20)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == matrix[i][j]:
                    color = 'white'
                else:
                    color = 'green'
                entry = tk.Text(root, fg='black', bg=color, font=font_style)
                entry.place(x=j*(500/9), y=i*(500/9))
                entry.insert(tk.END, matrix[i][j])
        for i in range(1, 3):
            frame1 = tk.Frame(root, highlightbackground="black", \
                highlightthickness=1, width=2, height=500)
            frame2 = tk.Frame(root, highlightbackground="black", \
                highlightthickness=1, width=500, height=2)
            frame1.place(x=500*i/3, y=0)
            frame2.place(x=0, y=500*i/3)
        root.mainloop()


    @staticmethod
    def draw_no_solution():
        """Shows a label with a message that there is no solution."""
        root = tk.Tk()
        root.geometry("400x100")
        text = "There is no possible solution to solve sudoku"
        tk.Label(root, text=text, font=("Lucida Grande", 14)).pack(pady=20)
        root.mainloop()


    def solve_sudoku(self):
        """Solves sudoku and draws it if thre is solution."""
        solution = self.sudoku.backtracking()
        if solution:
            self.draw_matrix(solution)
        else:
            self.draw_no_solution()


if __name__ == '__main__':
    sudoku_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    drawer = SudokuDrawer(sudoku_board)
    drawer.solve_sudoku()
