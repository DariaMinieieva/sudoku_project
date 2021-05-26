from stack import Stack
from arrays import Array2D
ways = 0


class CrosswordSolver:
    def __init__(self, matrix, words):
        self.matrix = matrix
        self.num_rows = self.matrix.num_rows()
        self.num_cols = self.matrix.num_cols()
        self.words = words
        self.ways = 0
        self.matrix_results = None
        self.possible_placements = []

    def get_empty(self):
        res = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i, j] == "-":
                    res.append((i, j))

        return res

    def place_words(self):
        used_words = Stack()
        words = self.words
        empty = self.get_empty()
        matrix_copy = self.matrix.copy()
        placements = self.count_words()
        start_point = placements[0]
        placements.remove(placements[0])

        while len(empty):
            pass

    def count_words(self):
        for i in range(self.num_rows):
            cont_word = 0
            ind_y = 0
            for j in range(self.num_cols):
                if self.matrix[i, j] == "-":
                    cont_word += 1
                else:
                    if cont_word >= 3:
                        self.possible_placements.append(
                            ("h", (i, ind_y), cont_word))

                    ind_y = j+1

                    cont_word = 0

            if cont_word >= 3:
                self.possible_placements.append(("h", (i, ind_y), cont_word))

        for i in range(self.num_cols):
            cont_word = 0
            ind_x = 0
            for j in range(self.num_rows):
                if self.matrix[j, i] == "-":
                    cont_word += 1
                else:
                    if cont_word >= 3:
                        self.possible_placements.append(
                            "v", (ind_x, i), cont_word)

                    ind_x = j+1

                    cont_word = 0

            if cont_word >= 3:
                self.possible_placements.append(("v", (ind_x, i), cont_word))

        return self.possible_placements

    def __str__(self):
        res = []

        for i in range(self.num_rows):
            temp = ""
            for j in range(self.num_cols):
                temp += self.matrix[i, j]

            res.append(temp)

        return "\n".join(res)


if __name__ == "__main__":
    test = Array2D(4, 4)
    test[0, 0] = "-"
    test[0, 1] = "-"
    test[0, 2] = "-"
    test[0, 3] = "-"
    test[1, 0] = "+"
    test[1, 1] = "-"
    test[1, 2] = "+"
    test[1, 3] = "+"
    test[2, 0] = "-"
    test[2, 1] = "-"
    test[2, 2] = "-"
    test[2, 3] = "-"
    test[3, 0] = "-"
    test[3, 1] = "-"
    test[3, 2] = "-"
    test[3, 3] = "-"
    cs = CrosswordSolver(test, ["day"])

    print(cs)
    print(cs.count_words())
