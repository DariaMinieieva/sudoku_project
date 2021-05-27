from arrays import Array2D
from copy import deepcopy
ways = 0


class CrosswordSolver:
    def __init__(self, matrix, words=None):
        self.matrix = matrix
        self.num_rows = self.matrix.num_rows()
        self.num_cols = self.matrix.num_cols()
        self.words = words
        self.ways = 0
        self.matrix_results = set()
        self.possible_placements = []

    def set_words(self, words):
        self.words = words

    def get_empty(self):
        res = []
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i, j] == "-":
                    res.append((i, j))

        return res

    def place_words(self):
        words = self.words.copy()

        placements = self.count_words()

        def helper(ind, placements, matrix, words):
            # print(CrosswordSolver(matrix), "\n")
            if ind < len(words):

                for place in placements:
                    matrix_copy = matrix.copy()

                    curr_word = words[ind]
                    if place[2] >= len(curr_word) and place[3] == "f":
                        if place[0] == "h":
                            count = 0
                            for i in range(place[1][1], len(curr_word)+place[1][1]):
                                if matrix_copy[place[1][0], i] != "-" and matrix_copy[place[1][0], i] != curr_word[count]:
                                    break
                                count += 1
                            else:
                                count = 0
                                for i in range(place[1][1], len(curr_word)+place[1][1]):
                                    matrix_copy[place[1][0],
                                                i] = curr_word[count]
                                    count += 1

                                helper(ind+1, placements,
                                       matrix_copy, words)

                        else:
                            count = 0
                            for i in range(place[1][0], len(curr_word)+place[1][0]):
                                if matrix_copy[i, place[1][1]] != "-" and matrix_copy[i, place[1][1]] != curr_word[count]:
                                    break
                                count += 1
                            else:
                                count = 0
                                for i in range(place[1][0], len(curr_word)+place[1][0]):
                                    # print(count)
                                    # print(curr_word)
                                    matrix_copy[i, place[1][1]
                                                ] = curr_word[count]
                                    count += 1

                                helper(ind+1, placements,
                                       matrix_copy, words)
            else:
                self.matrix_results.add(CrosswordSolver(matrix))

        helper(0, placements, self.matrix, words)

    def remove_wrong_indices(self, matrix, letters_indices, wrong):
        letters_to_remove = letters_indices[wrong]
        letters_to_leave = []

        letters_indices.pop(wrong)

        for i in letters_indices:
            for j in letters_indices[i]:
                letters_to_leave.append(j)

        for i in letters_to_remove:
            if i not in letters_to_leave:
                matrix[i[0], i[1]] = "-"

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
                            ["h", (i, ind_y), cont_word, "f"])

                    ind_y = j+1

                    cont_word = 0

            if cont_word >= 3:
                self.possible_placements.append(
                    ["h", (i, ind_y), cont_word, "f"])

        for i in range(self.num_cols):
            cont_word = 0
            ind_x = 0
            for j in range(self.num_rows):
                if self.matrix[j, i] == "-":
                    cont_word += 1
                else:
                    if cont_word >= 3:
                        self.possible_placements.append(
                            ["v", (ind_x, i), cont_word, "f"])

                    ind_x = j+1

                    cont_word = 0

            if cont_word >= 3:
                self.possible_placements.append(
                    ["v", (ind_x, i), cont_word, "f"])

        return self.possible_placements

    def __str__(self):
        res = []

        for i in range(self.num_rows):
            temp = ""
            for j in range(self.num_cols):
                temp += self.matrix[i, j]

            res.append(temp)

        return "\n".join(res)

    def __eq__(self, other):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i, j] != other.matrix[i, j]:
                    return False

        return True

    def __hash__(self):
        return hash(str(self))


if __name__ == "__main__":
    from random import shuffle
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
    cs = CrosswordSolver(test)
    test_list = ["home", "adoa", "aadd", "day"]
    shuffle(test_list)
    cs.set_words(test_list)

    print(cs, "\n")
    # print(cs.count_words())
    cs.place_words()
    for i in cs.matrix_results:
        print(i, "\n")
