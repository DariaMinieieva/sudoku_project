'''This module implements searching of the path in the maze using backtracking'''
from arrays import Array2D
from lliststack import Stack

class Maze:
    '''This class represents Maze using a 2-D array'''
    def __init__(self, path: str) -> None:
        with open(path, mode='r', encoding='utf-8') as file:
            (num_rows, num_cols) = self.read_two_values(file)
            self.array = Array2D(num_rows, num_cols)
            start_coord = self.read_two_values(file)
            end_coord = self.read_two_values(file)
            self.read_maze(file)
        self.start = self.array[start_coord[0], start_coord[1]]
        self.end = self.array[end_coord[0], end_coord[1]]

    def num_rows(self):
        '''Returns the number of rows in the maze'''
        return self.array.num_rows()

    def num_cols(self):
        '''Returns the number of columns in the maze'''
        return self.array.num_cols()

    def read_maze(self, file):
        '''Read maze from file'''
        for row in range(self.num_rows()):
            line = file.readline()
            for col in range(self.num_cols()):
                if line[col] == '*':
                    cell = Wall(row, col)
                else:
                    cell = Passage(row, col)
                    if row > 0:
                        left_cell = self.array[row-1, col]
                        if isinstance(left_cell, Passage):
                            cell.left = left_cell
                            left_cell.right = cell
                    if col > 0:
                        top_cell = self.array[row, col-1]
                        if isinstance(top_cell, Passage):
                            cell.top = top_cell
                            top_cell.down = cell
                self.array[row, col] = cell


    def read_two_values(self, file):
        '''Reads and formats a line from a file into tuple of two integer values'''
        line = file.readline()
        line = line.strip()
        first, second = map(int, line.split())
        return (first, second)

    def exit_found(self, cell):
        '''Method to determine if the exit was found.'''
        return cell == self.end

    def valid_move(self, cell):
        '''Return True if move is valid and False otherwise'''
        return cell is not None and cell.mark == '_'

    def find_path(self):
        '''
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        '''
        current = self.start
        stack = Stack()
        stack.push(current)

        while not self.exit_found(current) and not stack.is_empty():
            current = stack.peek()
            current.mark_path()
            impasse = True

            next_cell = current.right
            if self.valid_move(next_cell):
                stack.push(next_cell)
                impasse = False

            next_cell = current.down
            if self.valid_move(next_cell):
                stack.push(next_cell)
                impasse = False

            next_cell = current.left
            if self.valid_move(next_cell):
                stack.push(next_cell)
                impasse = False

            next_cell = current.top
            if self.valid_move(next_cell):
                stack.push(next_cell)
                impasse = False

            if impasse:
                current.mark_tried()
                stack.pop()

        if stack.is_empty():
            return False

        current.mark_path()
        return True

    def clear(self):
        '''Clear the maze by removing all 'path' and 'tried' tokens.'''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                cell = self.array[row, col]
                if isinstance(cell, Passage):
                    cell.clear_mark()

    def __str__(self):
        '''Returns a text-based representation of the maze.'''
        string = ''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                string += str(self.array[row, col]) + ' '
            string += '\n'
        return string


class Cell:
    '''This class represents cell of the maze'''
    def __init__(self, row, col) -> None:
        self.mark = None
        self.row = row
        self.col = col

    def __str__(self):
        '''Return string representing a cell'''
        return str(self.mark)

    def __eq__(self, other):
        '''Return True if two cells are equal and False otherwise'''
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        '''Return False if two cells are equal and True otherwise'''
        return not self == other


class Passage(Cell):
    '''
    This class represents cell of the maze which is a passage
    Connected with others cells in 4 directions
    '''
    PATH_TOKEN = 'x'
    TRIED_TOKEN = 'o'

    def __init__(self, row, col) -> None:
        super().__init__(row, col)
        self.right = None
        self.down = None
        self.left = None
        self.top = None
        self.clear_mark()

    def mark_tried(self):
        '''Drops a 'tried' token at the given cell.'''
        self.mark = self.TRIED_TOKEN

    def mark_path(self):
        '''Drops a 'path' token at the given cell.'''
        self.mark = self.PATH_TOKEN

    def clear_mark(self):
        '''Clear mark of the cell'''
        self.mark = '_'


class Wall(Cell):
    '''This class represents cell of the maze which is a wall'''
    def __init__(self, row, col) -> None:
        super().__init__(row, col)
        self.mark = '*'


if __name__ == '__main__':
    maze = Maze('maze_file.txt')
    print(maze.find_path())
    print(maze)
