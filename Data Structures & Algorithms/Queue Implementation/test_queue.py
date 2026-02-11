"""

Author: Dele Osuma
Queue Testing
unit tests for the Queue class.
"""

import unittest
import numpy as np
from queue import Queue, Empty

class TestQueue(unittest.TestCase):
    """
    Unit tests for the Queue class.
    """

    def setUp(self):
        """
        Initializes a new Queue instance for each test.
        """
        self.queue = Queue(3)  # Small capacity to trigger resizing
    
    def test_enqueue_dequeue(self):
        """
        Tests enqueue and dequeue operations.
        """
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.enqueue(30)

        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.dequeue(), 20)
        self.assertEqual(self.queue.dequeue(), 30)
        self.assertTrue(self.queue.is_empty())

    def test_peek(self):
        """
        Tests peeking at the front item without removing it.
        """
        self.queue.enqueue(5)
        self.assertEqual(self.queue.peek(), 5)
        self.assertEqual(len(self.queue), 1)

    def test_is_empty(self):
        """
        Tests if is_empty() correctly identifies an empty queue.
        """
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(7)
        self.assertFalse(self.queue.is_empty())
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())

    def test_empty_exception(self):
        """
        Tests that dequeue and peek raise Empty exception when the queue is empty.
        """
        with self.assertRaises(Empty):
            self.queue.dequeue()
        with self.assertRaises(Empty):
            self.queue.peek()

    def test_resize(self):
        """
        Tests if the queue resizes dynamically when full.
        """
        for i in range(6):  # Exceeds initial capacity
            self.queue.enqueue(i)

        self.assertEqual(len(self.queue), 6)
        for i in range(6):
            self.assertEqual(self.queue.dequeue(), i)

        self.assertTrue(self.queue.is_empty())

    def test_circular_behavior(self):
        """
        Tests that the queue correctly wraps around when elements are removed.
        """
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)

        self.queue.dequeue()  # Remove first element
        self.queue.enqueue(4)  # Add another to wrap around

        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertEqual(self.queue.dequeue(), 4)

    def test_resize_multiple_times(self):
        """
        Tests that queue correctly handles resizing beyond twice the original capacity.
        """
        for i in range(15):  # Exceed initial and doubled capacity
            self.queue.enqueue(i)

        for i in range(15):
            self.assertEqual(self.queue.dequeue(), i)

        self.assertTrue(self.queue.is_empty())

