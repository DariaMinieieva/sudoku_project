'''Implementation of the Stack ADT using a singly linked list.'''

class Stack:
    '''Creates an empty stack.'''
    def __init__(self):
        self._top = None
        self._size = 0

    def is_empty(self):
        '''Returns True if the stack is empty or False otherwise.'''
        return self._top is None

    def __len__(self):
        '''Returns the number of items in the stack.'''
        return self._size

    def peek(self):
        '''Returns the top item on the stack without removing it.'''
        assert not self.is_empty(), "Cannot peek at an empty stack"
        return self._top.item

    def pop(self):
        '''Removes and returns the top item on the stack.'''
        assert not self.is_empty(), "Cannot pop from an empty stack"
        node = self._top
        self._top = self._top.next
        self._size -= 1
        return node.item

    def push(self, item):
        '''Pushes an item onto the top of the stack.'''
        self._top = _StackNode(item, self._top)
        self._size += 1


class _StackNode:
    '''The private storage class for creating stack nodes.'''
    def __init__(self, item, link):
        self.item = item
        self.next = link
