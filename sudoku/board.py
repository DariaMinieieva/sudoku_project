"""This module implements backtracking algorithm to solve sudoku."""

class Board:
    """
    Class for sudoku board representation.
    """
    NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


    def __init__(self, board):
        """
        Create a new board.
        """
        self.board = board


    def __str__(self) -> str:
        """
        Return string reprentation of a board.
        """
        result = ''
        for line in self.board:
            result += str(line) + '\n'
        return result.strip()


    @staticmethod
    def check_rows(board) -> bool:
        """
        Check if rows are filled correctly and don't have empty cells.
        """
        for row in board:
            numbers = list(range(1,10))
            for cell in row:
                if cell in numbers:
                    numbers.remove(cell)
                else:
                    return False
        return True


    def check_colums(self) -> bool:
        """
        Check if colums are filled correctly and don't have empty cells.
        """
        board_1 = [[self.board[i][j] for i in range(9)] for j in range(9)]
        return self.check_rows(board_1)


    def check_subgrids(self) -> bool:
        """
        Check if subgrids are filled correctly and don't have empty cells.
        """
        board_2 = [[self.board[i][j], self.board[i][j+1], self.board[i][j+2],
                    self.board[i+1][j], self.board[i+1][j+1], self.board[i+1][j+2],
                    self.board[i+2][j], self.board[i+2][j+1], self.board[i+2][j+2]] \
                        for i in range(0, 9, 3) for j in range(0, 9, 3)]
        return self.check_rows(board_2)


    def check_board(self) -> bool:
        """
        Check if board if filled correctly and doesn't have empty words.
        """
        return self.check_rows(self.board) and self.check_colums() and self.check_subgrids()


    def get_cell(self) -> tuple or None:
        """
        Return coordinates of a first empty cell.
        """
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    return row, column


    @staticmethod
    def filter_values(values, used) -> set:
        """
        Return set of valid numbers from values that do not appear in used
        """
        return set([number for number in values if number not in used])


    def filter_row(self, row) -> set:
        """
        Return set of numbers that can be placed into a certain row.
        """
        in_row = [number for number in self.board[row] if number != 0]
        options = self.filter_values(self.NUMBERS, in_row)
        return options


    def filter_column(self, column) -> set:
        """
        Return set of numbers that can be placed into a certain column.
        """
        in_column = [self.board[i][column] for i in range(9)]
        options = self.filter_values(self.NUMBERS, in_column)
        return options


    def filter_subgrid(self, row: int, column: int) -> set:
        """
        Return set of numbers that can be placed into a certain subgrid.
        """
        row_start = int(row / 3) * 3
        column_start = int(column / 3) * 3
        in_subgrid = []
        for i in range(3):
            for j in range(3):
                in_subgrid.append(self.board[row_start+i][column_start+j])
        options = self.filter_values(self.NUMBERS, in_subgrid)
        return options


    def available_options(self, row: int, column: int) -> list:
        """
        Return a list of possible numbers that can be placed into a cell.
        """
        for_row = self.filter_row(row)
        for_column = self.filter_column(column)
        for_subgrid = self.filter_subgrid(row, column)
        result = for_row.intersection(for_column, for_subgrid)
        return list(result)


    def backtracking(self) -> list or None:
        """
        Main function that implements backtracking algorithm to solve sudoku.
        """
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
            self.board[row][column] = 0  # otherwise backtracks
