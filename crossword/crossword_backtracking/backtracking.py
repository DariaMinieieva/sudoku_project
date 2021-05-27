"""This module implements backtracking algorithm to solve crossword."""

# from arrays import Array2D

class CrosswordSolver:
    """Class for crossword solving representation."""


    def __init__(self, matrix: 'Array2D', words=None):
        """Creates a new crossword solver."""
        self.matrix = matrix
        self.num_rows = self.matrix.num_rows()
        self.num_cols = self.matrix.num_cols()
        self.words = words
        self.matrix_results = set()
        self.possible_placements = []


    def set_words(self, words: list):
        """Sets the words to be in the crossword from list."""
        self.words = words


    def place_words(self):
        """
        Main function that implements backtracking algorithm to find
        possible ways to solve the crossword. Uses recursive helper function.
        """
        words = self.words.copy()
        placements = self.place_possible()

        def helper(ind, placements, matrix, words):
            if ind < len(words):

                for place in placements:
                    matrix_copy = matrix.copy()

                    curr_word = words[ind]
                    if place[2] >= len(curr_word) and place[3] == "f":
                        if place[0] == "h":
                            count = 0
                            for i in range(place[1][1], len(curr_word)+place[1][1]):
                                if matrix_copy[place[1][0], i] != "-" and \
                                    matrix_copy[place[1][0], i] != curr_word[count]:
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
                                if matrix_copy[i, place[1][1]] != "-" and \
                                    matrix_copy[i, place[1][1]] != curr_word[count]:
                                    break
                                count += 1
                            else:
                                count = 0
                                for i in range(place[1][0], len(curr_word)+place[1][0]):
                                    matrix_copy[i, place[1][1]
                                                ] = curr_word[count]
                                    count += 1

                                helper(ind+1, placements,
                                       matrix_copy, words)
            else:
                self.matrix_results.add(CrosswordSolver(matrix))

        helper(0, placements, self.matrix, words)


    def place_possible(self):
        """Describes the crossword grid by finding free places
        to set the words and returns them as a list."""
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
        """Returns a string representation of a crossword."""
        res = []

        for i in range(self.num_rows):
            temp = ""
            for j in range(self.num_cols):
                temp += self.matrix[i, j]

            res.append(temp)

        return "\n".join(res)


    def __eq__(self, other):
        """Compares two crosswords and returns True if they are the same or False otherwise."""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.matrix[i, j] != other.matrix[i, j]:
                    return False

        return True

    def __hash__(self):
        """Returns a hashable object of crossword."""
        return hash(str(self))
