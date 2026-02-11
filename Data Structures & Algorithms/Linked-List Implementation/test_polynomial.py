# test_polynomial.py

import unittest
from polynomial import *


# Run from terminal: python -m unittest test_polynomial.py
class PolynomialTest(unittest.TestCase):

    def test_term_basic(self):
        t = Term(7, 8)
        self.assertEqual(t.get_next(), None)
        t1 = Term(7, 8)
        self.assertTrue(t == t1)
        t2 = Term(-7, 8)
        self.assertFalse(t == t2)

    def test_term_str(self):
        constant = Term(5, 0)
        self.assertEqual('5', str(constant))

        _7x_5 = Term(7, 5)
        self.assertEqual('7x^5', str(_7x_5))

        neg_7x_5 = Term(-7, 5)
        self.assertEqual('-7x^5', str(neg_7x_5))

    def test_simple(self):
        p1 = Polynomial()
        self.assertEqual('0', str(p1))

        p2 = Polynomial([(1, 2)])
        self.assertEqual('x^2', str(p2))

        p3 = Polynomial([(1, 0), (6, 1), (5, 2), (2, 3)])
        self.assertEqual('2x^3 + 5x^2 + 6x + 1', str(p3))

    def test_order(self):
        p1 = Polynomial([(1, 2), (4, 0)])
        self.assertEqual('x^2 + 4', str(p1))

        p2 = Polynomial([(1, 5), (0, 2), (4, 0), (-3, 3), (1, 1)])
        self.assertEqual('x^5 - 3x^3 + x + 4', str(p2))

        p3 = Polynomial([(0, 2), (-4, 3), (-5, 6)])
        self.assertEqual('-5x^6 - 4x^3', str(p3))

    def test_get_first(self):
        p1 = Polynomial([(1, 2), (4, 0)])
        self.assertEqual(p1.get_first(), Term(1, 2))

        p2 = Polynomial([(-1, 7), (-5, 3), (4, 2)])
        self.assertEqual(p2.get_first(), Term(-1, 7))

    def test_zero(self):
        p1 = Polynomial([(0, 0)])
        self.assertTrue(p1.iszero())

        p2 = Polynomial([(1, 5), (0, 2), (4, 0), (3, 3), (1, 1)])
        self.assertFalse(p2.iszero())

    def test_lowest_term(self):
        p1 = Polynomial([(0, 0)])
        self.assertEqual(0, p1.lowest_term())

        p2 = Polynomial([(-1, 7), (-5, 3), (4, 2)])
        self.assertEqual(2, p2.lowest_term())

    def test_degree(self):
        p1 = Polynomial([(0, 0)])
        self.assertEqual(0, p1.degree())

        p2 = Polynomial([(-1, 7), (-5, 3), (4, 2), (7, 0)])
        self.assertEqual(7, p2.degree())

    def test_collect_terms(self):
        p1 = Polynomial([(1, 2), (-4, 2)])
        self.assertEqual('-3x^2', str(p1))

        p2 = Polynomial([(1, 2), (0, 2), (-4, 0), (3, 3), (-1, 2), (-1, 1), (5, 3), (-8, 3)])
        self.assertEqual('-x - 4', str(p2))

    def test_second_highest_coefficient(self):
        p0 = Polynomial()
        p1 = Polynomial([(1, 1)])
        p2 = Polynomial([(1, 5), (3, 3), (7, 2), (1, 1), (4, 0)])
        p3 = Polynomial([(2, 5), (5, 4), (10, 1)])
        p4 = Polynomial([(-1, 3), (-2, 2), (-1, 1), (4, 0)])
        p5 = Polynomial([(1, 3), (2, 2), (1, 1), (4, 0)])
        self.assertEqual(None, p0.second_highest_coefficient())
        self.assertEqual(None, p1.second_highest_coefficient())
        self.assertEqual(4, p2.second_highest_coefficient())
        self.assertEqual(5, p3.second_highest_coefficient())
        self.assertEqual(-1, p4.second_highest_coefficient())
        self.assertEqual(2, p5.second_highest_coefficient())

    def test_add(self):
        p0 = Polynomial()
        p1 = Polynomial([(1, 1)])
        p2 = Polynomial([(1, 5), (3, 3), (7, 2), (1, 1), (4, 0)])
        p3 = Polynomial([(2, 5), (-1, 4), (-3, 1)])
        p4 = Polynomial([(-1, 3), (2, 2), (-1, 1), (-4, 0)])
        p5 = Polynomial([(1, 3), (-2, 2), (1, 1), (4, 0)])

        self.assertEqual('x', str(p0 + p1))
        self.assertEqual('2x^5 - x^4 - 3x', str(p0 + p3))
        self.assertEqual('x^5 + 3x^3 + 7x^2 + 2x + 4', str(p1 + p2))
        self.assertEqual('3x^5 - x^4 + 3x^3 + 7x^2 - 2x + 4', str(p2 + p3))
        self.assertEqual('2x^5 - x^4 - x^3 + 2x^2 - 4x - 4', str(p3 + p4))
        self.assertEqual('0', str(p4 + p5))


if __name__ == '__main__':
    unittest.main()
