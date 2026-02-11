import unittest
from table import *


# Run from terminal: python -m unittest test_table.py
class TableTest(unittest.TestCase):
    def setUp(self) -> None:
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.max_load_factor = 2/3

    def test_empty(self):
        """Test the attributes of an empty table"""
        t = Table()
        self.assertEqual(0, len(t))
        self.assertEqual(set(), t.keys())
        self.assertEqual('{}', str(t))
        self.assertEqual(0, t.load())

    def test_exception(self):
        """Test that KeyError is raised when applicable"""
        t = Table(5)
        self.assertRaises(KeyError, t.get, 'hello')
        self.assertRaises(KeyError, t.remove, 'hello')

    def test_add(self):
        """Test the add method"""
        t = Table(5)
        counter = 1
        for key in ['hello', 'world', 'good', 'morning', 'great']:
            t.add(key, counter)
            t.add(key, counter)  # make sure it doesn't insert multiple entries
            self.assertEqual(counter, len(t))
            self.assertTrue(key in t.keys())
            counter += 1

    def test_load(self):
        """The load factor must be below 2/3 at all times"""
        t = Table(1)
        for key, value in enumerate(self.letters):
            t.add(key, value)
            self.assertTrue(t.load() < self.max_load_factor)

    def test_get(self):
        """Test the get method"""
        t = Table(3)
        t.add(101, 'Python I')
        t.add(103, 'Python II')
        t.add(200, 'Data Structures')
        self.assertEqual('Python I', t.get(101))
        self.assertEqual('Python II', t.get(103))
        self.assertEqual('Data Structures', t.get(200))
        self.assertRaises(KeyError, t.get, 500)
        self.assertEqual(3, len(t))
        self.assertTrue(len(t) == len(t.keys()))

    def test_keys_length(self):
        """Test the keys and len methods"""
        t = Table(50)
        self.assertEqual(0, len(t.keys()))
        self.assertEqual(0, len(t))

        for key, value in enumerate(self.letters):
            t.add(key, value)
            self.assertTrue(key in t.keys())

        self.assertEqual(len(self.letters), len(t.keys()))
        self.assertEqual(len(self.letters), len(t))

    def test_remove(self):
        """Test the remove method"""
        t = Table(10)
        for letter in self.letters:
            t.add(letter, 0)
            self.assertTrue(letter in t.keys())

        entries = len(self.letters)
        for letter in self.letters:
            t.remove(letter)
            entries -= 1

            self.assertFalse(letter in t.keys())
            self.assertRaises(KeyError, t.get, letter)
            self.assertEqual(entries, len(t))
            self.assertEqual(entries, len(t.keys()))

    def test_str(self):
        """Test the str method.

        Since keys are stored in a set, the order of entries is unpredictable.
        As long as key: value pairs are in the returned value of the str method,
        the method is considered working correctly.
        """
        t = Table()
        t.add('hello', 'world')
        self.assertEqual('{<hello: world>}', str(t))

        for value, key in enumerate(self.letters):
            t.add(key, value)
            self.assertTrue(f'{key}: {value}' in str(t))

    def test_misc(self):
        """Test various features of a table"""
        grade = Table(3)
        grade.add('CMPT 101', 'A')
        grade.add('CMPT 103', 'B')
        grade.add('CMPT 200', 'B+')
        grade.add('CMPT 201', 'B-')

        self.assertEqual('A', grade.get('CMPT 101'))
        self.assertEqual(4, len(grade))
        self.assertEqual(len(grade), len(grade.keys()))
        self.assertTrue(grade.load() < self.max_load_factor)

        grade.add('CMPT 101', 'A+')  # change grade from A to A+
        self.assertEqual('A+', grade.get('CMPT 101'))

        grade.remove('CMPT 101')
        self.assertEqual(3, len(grade))
        self.assertEqual(len(grade), len(grade.keys()))
        self.assertTrue('CMPT 101' not in grade.keys())
        self.assertRaises(KeyError, grade.get, 'CMPT 101')
        self.assertRaises(KeyError, grade.remove, 'CMPT 101')
        
    def test_show_entries(self):
        """Test the _print_table method"""
        t = Table(10)
        for letter in self.letters:
            t.add(letter, 0)
            self.assertTrue(letter in t.keys())

        for letter in self.letters:
            t.remove(letter)
            
        t._show_entries()        
if __name__ == '__main__':
    unittest.main()