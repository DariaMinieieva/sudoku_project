"""
This module is the main module for the crossword
and serves for the crossword solving.
"""

import random
from arrays import Array2D
from backtracking import CrosswordSolver


def choose_mode() -> int:
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
        mode = choose_mode()
    return mode


def get_random(file: str, words_num: int) -> list:
    """Returns random words from file."""
    words = []
    with open(file, encoding='utf-8') as words_f:
        for word in words_f:
            words.append(word.strip().upper())
    random.shuffle(words)
    final_words = []
    left = words_num
    while left:
        word = words.pop()
        if len(word) > 2:
            final_words.append(word)
            left -= 1
    return final_words


def get_user_words(words_num: int) -> list:
    """Returns list of user words."""
    words = []
    left = words_num
    while left:
        print(f'You have {left} words left to enter.')
        word = input("Enter the word to be in the crossword: ")
        if len(word) < 3:
            print("Word must must be not shorter than 3 symbols.")
        else:
            words.append(word.upper())
            left -= 1
    return words


def read_matrix(file: str):
    """Returns a 2D Array with the grid for crossword that is read from file."""
    with open(file, encoding='utf-8') as grid_f:
        num_row, num_col = map(int, grid_f.readline().split())
        grid = Array2D(num_row, num_col)
        row_pos = 0
        for row in grid_f:
            for col_pos in range(num_col):
                grid[row_pos, col_pos] = row[col_pos]
            row_pos += 1
    return grid


def solve_crossword(matrix_file: str):
    """Main function that solves the crossword."""
    matrix = read_matrix(matrix_file)
    solver = CrosswordSolver(matrix)
    words_num = len(solver.count_words())
    mode = choose_mode()
    if mode == 1:
        words = get_user_words(words_num)
    else:
        words = get_random('words.txt')
    solver.words = words
    solver.place_words()


if __name__ == "__main__":
    solve_crossword('grid.txt')
