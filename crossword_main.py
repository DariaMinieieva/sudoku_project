"""
This module is the main module for the crossword
and serves for the crossword solving.
"""

import random
from arrays import Array2D


# solver = CrosswordSolver()
# words_num = solver.count_words()


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


def get_random(file: str, words_num: int) -> set:
    """Returns random words from file."""
    words = []
    with open(file, encoding='utf-8') as words_f:
        for word in words_f:
            words.append(word.strip().upper())
    random.shuffle(words)
    return words[:words_num]


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


# print(choose_mode())
# print(get_random('words.txt', 5))
# print(read_matrix('grid.txt')[9, 9])
