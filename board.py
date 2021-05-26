class Board:
    NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, board):
        self.board = board

    def __str__(self):
        """
        Return string reprentation of a board.
        """
        result = ''
        for line in self.board:
            result += str(line) + '\n'
        return result.strip()

    def check_rows(self, board):
        """
        Check if rows are filled correctly and don't have empty cells.
        """
        for row in board:
            numbers = [i for i in range(1,10)]
            for cell in row:
                if cell in numbers:
                    numbers.remove(cell)
                else:
                    return False
        return True

    def check_colums(self):
        """
        Check if colums are filled correctly and don't have empty cells.
        """
        board_1 = [[self.board[i][j] for i in range(9)] for j in range(9)]
        return self.check_rows(board_1)

    def check_subgrids(self):
        """
        Check if subgrids are filled correctly and don't have empty cells.
        """
        board_2 = [[self.board[i][j], self.board[i][j+1], self.board[i][j+2],
                    self.board[i+1][j], self.board[i+1][j+1], self.board[i+1][j+2],
                    self.board[i+2][j], self.board[i+2][j+1], self.board[i+2][j+2]] for i in range(0, 9, 3) for j in range(0, 9, 3)]
        return self.check_rows(board_2)

    def check_board(self):
        """
        Check if board if filled correctly and doesn't have empty words.
        """
        return self.check_rows(self.board) and self.check_colums() and self.check_subgrids()

    def get_cell(self):
        """
        Return coordinates of a first empty cell.
        """
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    return row, column

    def filter_values(self, values, used):
        """
        Return set of valid numbers from values that do not appear in used
        """
        return set([number for number in values if number not in used])

    def filter_row(self, row):
        in_row = [number for number in self.board[row] if (number != 0)]
        options = self.filter_values(self.NUMBERS, in_row)
        return options

    def filter_column(self, column):
        in_column = [self.board[i][column] for i in range(9)]
        options = self.filter_values(self.NUMBERS, in_column)
        return options

    def filter_subgrid(self, row, column):
        row_start = int(row / 3) * 3
        column_start = int(column / 3) * 3
        in_subgrid = []
        for i in range(3):
            for j in range(3):
                in_subgrid.append(self.board[row_start+i][column_start+j])
        options = self.filter_values(self.NUMBERS, in_subgrid)
        return options

    def available_options(self, row, column):
        for_row = self.filter_row(row)
        for_column = self.filter_column(column)
        for_subgrid = self.filter_subgrid(row, column)
        result = for_row.intersection(for_column, for_subgrid)
        return list(result)

    def backtracking(self):
        if self.check_board():
            return self.board
        # get first empty cell
        row, column = self.get_cell()
        # get viable options
        options = self.available_options(row, column)

        for option in options:
            self.board[row][column] = option  # try viable option
            # recursively fill in the board
            if self.backtracking():
                return self.board  # return board if success
            else:
                self.board[row][column] = 0  # otherwise backtracks


def solve_sudoku(board):
    sudoku = Board(board)
    solution = sudoku.backtracking()
    if solution:
        return solution
    else:
        return "No possible solutions"


board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]
print(solve_sudoku(board))
