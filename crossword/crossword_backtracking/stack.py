'''
Implementation of the Stack ADT using a singly linked list.

This code is taken from  https://github.com/anrom7/Stack 
'''


class Stack:
    # Creates an empty stack.
    def __init__(self):
        self._top = None
        self._size = 0

    # Returns True if the stack is empty or False otherwise.
    def is_empty(self):
        return self._top is None

    # Returns the number of items in the stack.
    def __len__(self):
        return self._size

    # Returns the top item on the stack without removing it.
    def peek(self):
        assert not self.is_empty(), "Cannot peek at an empty stack"
        return self._top.item

    # Removes and returns the top item on the stack.
    def pop(self):
        assert not self.is_empty(), "Cannot pop from an empty stack"
        node = self._top
        self._top = self._top.next
        self._size -= 1
        return node.item

    # Pushes an item onto the top of the stack.
    def push(self, item):
        self._top = _StackNode(item, self._top)
        self._size += 1


# The private storage class for creating stack nodes.
class _StackNode:
    def __init__(self, item, link):
        self.item = item
        self.next = link
