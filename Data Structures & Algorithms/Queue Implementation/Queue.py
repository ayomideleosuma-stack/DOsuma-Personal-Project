"""
queue.py
Author: Dele Osuma

Tmplementing an array-based dynamic circular queue using numpy.
"""

import numpy as np

class Empty(Exception):
    """Custom exception to indicate queue is empty."""
    pass

class Queue:
    """
    Implements an array-based circular queue using numpy.
    Expands dynamically when full.
    """

    def __init__(self, capacity=5):
        """
        Initializes a circular queue with a fixed capacity.

        Parameters:
        - capacity (int): The initial capacity of the queue (default: 5).
        
        Post-condition:
        - Creates an empty queue with the given capacity.
        """
        self._data = np.empty(capacity, dtype=object)
        self._capacity = capacity
        self._size = 0
        self._front = 0
        self._rear = 0

    def enqueue(self, item):
        """
        Adds an item to the queue. Resizes if necessary.

        Parameters:
        - item (object): The item to be added to the queue.
        
        Post-condition:
        - The item is added to the rear of the queue.
        - Queue resizes dynamically if full.
        """
        if self._size == self._capacity:
            self._resize()
        self._data[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the front item of the queue.

        Raises:
        - Empty: If the queue is empty.

        Returns:
        - The front item of the queue.

        Post-condition:
        - The front item is removed from the queue.
        - The queue size is reduced.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        item = self._data[self._front]
        self._data[self._front] = None  # Avoid memory retention issues
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item

    def peek(self):
        """
        Returns the front item without removing it.

        Raises:
        - Empty: If the queue is empty.

        Returns:
        - The front item of the queue.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[self._front]

    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
        - (bool): True if empty, False otherwise.
        """
        return self._size == 0

    def __len__(self):
        """
        Returns the number of elements in the queue.

        Returns:
        - (int): The current size of the queue.
        """
        return self._size

    def __repr__(self):
        """
        Returns a string representation of the queue.

        Returns:
        - (str): The queue elements from front to rear.
        """
        items = []
        for i in range(self._size):
            items.append(self._data[(self._front + i) % self._capacity])
        return f"Queue: {items}"

    def _resize(self):
        """
        Doubles the capacity of the queue when full.

        Post-condition:
        - The queue capacity is doubled.
        - The elements are copied to a new array in order.
        """
        new_capacity = self._capacity * 2
        new_data = np.empty(new_capacity, dtype=object)
        
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]

        self._data = new_data
        self._capacity = new_capacity
        self._front = 0
        self._rear = self._size  # Reset rear index after copying elements
