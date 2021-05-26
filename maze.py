from arrays import Array2D

class Maze:
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
        """Returns the number of rows in the maze."""
        return self.array.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self.array.num_cols()

    def read_maze(self, file):
        for row in range(self.num_rows()):
            line = file.readline()
            for col in range(self.num_cols()):
                if line[col] == '*':
                    self.array[row, col] = Wall()
                else:
                    self.array[row, col] = Passage()

    def read_two_values(self, file):
        '''Reads and formats a line from a file into tuple of two integer values'''
        line = file.readline()
        line = line.strip()
        first, second = map(int, line.split())
        return (first, second)

    def clear(self):
        """Clear the maze by removing all "path" and "tried" tokens."""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                cell = self.array[row, col]
                if isinstance(cell, Passage):
                    cell.clear_mark()


    def __str__(self):
        """Returns a text-based representation of the maze."""
        string = ''
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                string += str(self.array[row, col]) + ' '
            string += '\n'
        return string


class Cell:
    def __init__(self) -> None:
        self.mark = None

    def __str__(self):
        return self.mark


class Passage(Cell):
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self) -> None:
        super()
        self.clear_mark()

    def mark_tried(self):
        """Drops a "tried" token at the given cell."""
        self.mark = self.TRIED_TOKEN

    def mark_path(self):
        """Drops a "path" token at the given cell."""
        self.mark = self.PATH_TOKEN

    def clear_mark(self):
        self.mark = '_'


class Wall(Cell):
    def __init__(self) -> None:
        super()
        self.mark = '*'
