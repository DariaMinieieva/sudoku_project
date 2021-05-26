"""This module contains different arrays realisations."""

import ctypes


class Array:
    """Implements the Array ADT using array capabilities of the ctypes module."""

    def __init__(self, size):
        """Creates an array with size elements."""
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        py_array_type = ctypes.py_object * size
        self._elements = py_array_type()
        # Initialize each element.
        self.clear(None)

    def __len__(self):
        """Returns the size of the array."""
        return self._size

    def __getitem__(self, index):
        """Gets the contents of the index element."""
        assert 0 <= index < len(self), "Array subscript out of range"
        return self._elements[index]

    def __setitem__(self, index, value):
        """Puts the value in the array element at index position."""
        assert 0 <= index < len(self), "Array subscript out of range"
        self._elements[index] = value

    def clear(self, value):
        """Clears the array by setting each element to the given value."""
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        """Returns the array's iterator for traversing the elements."""
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """An iterator for the Array ADT."""

    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        raise StopIteration


class Array2D:
    """Implementation of the Array2D ADT using an array of arrays."""

    def __init__(self, num_rows, num_cols):
        """Creates a 2 -D array of size numRows x numCols."""
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    def num_rows(self):
        """Returns the number of rows in the 2 -D array."""
        return len(self.rows)

    def num_cols(self):
        """Returns the number of columns in the 2 -D array."""
        return len(self.rows[0])

    def clear(self, value):
        """Clears the array by setting every element to the given value."""
        for row in range(self.num_rows()):
            self.rows[row].clear(value)

    def __getitem__(self, index_tuple):
        """Gets the contents of the element at position [i, j]"""
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        return array_1d[col]

    def __setitem__(self, index_tuple, value):
        """Sets the contents of the element at position [i,j] to value."""
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert 0 <= row < self.num_rows() and 0 <= col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        array_1d[col] = value

    def copy(self):
        rows = self.num_rows()
        cols = self.num_cols()
        new_array = Array2D(rows, cols)

        for i in range(rows):
            for j in range(cols):
                new_array[i, j] = self[i, j]

        return new_array


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # count actual elements
        self._capacity = 1  # default array capacity
        self._array = self._make_array(self._capacity)  # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._array[k]  # retrieve from array

    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        self._array[self._n] = obj
        self._n += 1

    def _resize(self, capacity):  # nonpublic utitity
        """Resize internal array to capacity c."""
        bigger = self._make_array(capacity)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            bigger[k] = self._array[k]
        self._array = bigger  # use the bigger array
        self._capacity = capacity

    @staticmethod
    def _make_array(capacity):  # nonpublic utility
        """Return new array with capacity c."""
        return (capacity * ctypes.py_object)()  # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._array[j] = self._array[j - 1]
        self._array[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value( or  raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._array[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._array[j] = self._array[j + 1]
                self._array[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item

                return  # exit immediately
        raise ValueError("value not found")  # only reached if no match
