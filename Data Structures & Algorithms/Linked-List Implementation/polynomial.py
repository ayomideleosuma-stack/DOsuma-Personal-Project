"""
Author: Dele Osuma
Sparse polynomial linked-list implementation (Python).
Stores nonzero terms in a sorted linked list
Maintains canonical form, supports printing, key queries, and + addition with specified complexity guarantees.
"""

class Term:
    """
    single term in a polynomial

    Each Term has an integer coefficient, a nonnegative integer exponent,
    and a reference to the next Term in the linked list.
    """
    def __init__(self, coefficient, exponent, next_term=None):
        # Coefficient and exponent are integers, exponent are nonnegative.
        self.coefficient = coefficient
        self.exponent = exponent
        self._next = next_term

    def get_next(self):
        """
        Returns the next Term in the linked list.
        """
        return self._next

    def __eq__(self, other):
        """
        Two Terms are equal if they have the same coefficient and exponent.
        """
        if isinstance(other, Term):
            return self.coefficient == other.coefficient and self.exponent == other.exponent
        return False

    def __str__(self):
        """
        Returns a string representation of the term.
        
        Examples:
          Term(3, 0)   -> "3"
          Term(-1, 0)  -> "-1"
          Term(1, 1)   -> "x"
          Term(-1, 1)  -> "-x"
          Term(2, 1)   -> "2x"
          Term(3, 6)   -> "3x^6"
        """
        if self.exponent == 0:
            return str(self.coefficient)
        if self.exponent == 1:
            if self.coefficient == 1:
                return "x"
            elif self.coefficient == -1:
                return "-x"
            else:
                return str(self.coefficient) + "x"
        # For exponents greater than 1:
        if self.coefficient == 1:
            return "x^" + str(self.exponent)
        elif self.coefficient == -1:
            return "-x^" + str(self.exponent)
        else:
            return str(self.coefficient) + "x^" + str(self.exponent)


class Polynomial:
    """
    Represents an integer polynomial using a sorted linked list of Term objects.

    Nonzero terms are stored in canonical form (collected like terms and in
    descending order by exponent). A zero polynomial is represented by a single
    term: Term(0, 0).
    """
    def __init__(self, term_list=None):
        """
        Initializes a Polynomial from an optional list of (coefficient, exponent) tuples.

        Like terms are combined and zero-coefficient terms discarded. If no valid term is
        inserted, the polynomial is the zero polynomial.
        """
        self._head = None
        if term_list is not None:
            for tup in term_list:
                coeff = tup[0]
                exp = tup[1]
                if exp < 0:
                    raise ValueError("Exponent must be nonnegative")
                if coeff != 0:
                    self._insert_term(coeff, exp)
        if self._head is None:
            self._head = Term(0, 0)

    def _insert_term(self, coefficient, exponent):
        """
        Inserts a new term into the polynomial's linked list in descending order.

        If a term with the same exponent exists, their coefficients are added.
        If the sum becomes zero, the term is removed.
        """
        # if the polynomial is currently the zero polynomial,
        # replace it with the new nonzero term.
        if (self._head is not None and 
            self._head.coefficient == 0 and 
            self._head.exponent == 0 and 
            self._head.get_next() is None):
            if coefficient == 0:
                return
            else:
                self._head = Term(coefficient, exponent)
                return

        if self._head is None:
            self._head = Term(coefficient, exponent)
            return

        if exponent > self._head.exponent:
            new_term = Term(coefficient, exponent, self._head)
            self._head = new_term
            return

        prev = None
        current = self._head
        while current is not None and current.exponent > exponent:
            prev = current
            current = current.get_next()
        if current is not None and current.exponent == exponent:
            current.coefficient += coefficient
            if current.coefficient == 0:
                if prev is None:
                    self._head = current.get_next()
                    if self._head is None:
                        self._head = Term(0, 0)
                else:
                    prev._next = current.get_next()
            return
        new_term = Term(coefficient, exponent, current)
        if prev is None:
            self._head = new_term
        else:
            prev._next = new_term

    def __str__(self):
        """
        Returns the polynomial in canonical form as a string.

        Terms are printed in descending order and separated by " + " or " - ".
        The zero polynomial returns "0".
        """
        if self.iszero():
            return "0"
        result = ""
        current = self._head
        first = True
        while current is not None:
            if current.coefficient != 0:
                term_str = current.__str__()
                if first:
                    result = term_str
                    first = False
                else:
                    if current.coefficient < 0:
                        result = result + " - " + term_str[1:]
                    else:
                        result = result + " + " + term_str
            current = current.get_next()
        return result

    def iszero(self):
        """
        Returns True if the polynomial is the zero polynomial; otherwise, False.

        Runs in O(1) time.
        """
        return (self._head is not None and 
                self._head.coefficient == 0 and 
                self._head.exponent == 0 and 
                self._head.get_next() is None)

    def get_first(self):
        """
        Returns the first term (with the highest exponent) without modifying the polynomial.

        Runs in O(1) time.
        """
        return self._head

    def degree(self):
        """
        Returns the degree (the highest exponent) of the polynomial.

        For the zero polynomial, returns 0.
        Runs in O(1) time.
        """
        if self._head is None:
            return 0
        return self._head.exponent

    def lowest_term(self):
        """
        Returns the exponent of the lowest nonzero term in the polynomial.

        Runs in O(n) time.
        """
        current = self._head
        if current is None:
            return 0
        while current.get_next() is not None:
            current = current.get_next()
        return current.exponent

    def second_highest_coefficient(self):
        """
        Returns the second highest nonzero coefficient in the polynomial.
        
        If the highest coefficient occurs more than once, returns that highest value.
        If there is no second coefficient (e.g., zero polynomial or only one nonzero term),
        returns None.
        
        Runs in O(n) time using O(1) extra space.
        """
        # If the polynomial is zero or has a single nonzero term, return None.
        if self._head is None or self._head.get_next() is None:
            return None

        # First pass: find the highest coefficient and count its occurrences.
        max_coeff = None
        count_max = 0
        current = self._head
        while current is not None:
            if current.coefficient != 0:
                if max_coeff is None or current.coefficient > max_coeff:
                    max_coeff = current.coefficient
                    count_max = 1
                elif current.coefficient == max_coeff:
                    count_max += 1
            current = current.get_next()

        if max_coeff is None:
            return None

        # If highest occurs at least twice, return it.
        if count_max >= 2:
            return max_coeff

        # Otherwise, find the maximum among coefficients less than max_coeff.
        second = None
        current = self._head
        while current is not None:
            coeff = current.coefficient
            if coeff != 0 and coeff < max_coeff:
                if second is None or coeff > second:
                    second = coeff
            current = current.get_next()
        return second

    def __add__(self, other):
        """
        Returns a new Polynomial representing the sum of this polynomial and another.

        If the other operand is not a Polynomial, returns None.
        Runs in O(n) time using O(n) extra space.
        """
        if not isinstance(other, Polynomial):
            return None

        p1 = self._head
        p2 = other._head
        result_head = None
        result_tail = None

        def append_term(coeff, exp):
            nonlocal result_head, result_tail
            if coeff == 0:
                return
            new_node = Term(coeff, exp)
            if result_head is None:
                result_head = new_node
                result_tail = new_node
            else:
                result_tail._next = new_node
                result_tail = new_node

        while p1 is not None and p2 is not None:
            if p1.exponent > p2.exponent:
                append_term(p1.coefficient, p1.exponent)
                p1 = p1.get_next()
            elif p1.exponent < p2.exponent:
                append_term(p2.coefficient, p2.exponent)
                p2 = p2.get_next()
            else:
                sum_coeff = p1.coefficient + p2.coefficient
                if sum_coeff != 0:
                    append_term(sum_coeff, p1.exponent)
                p1 = p1.get_next()
                p2 = p2.get_next()
        while p1 is not None:
            append_term(p1.coefficient, p1.exponent)
            p1 = p1.get_next()
        while p2 is not None:
            append_term(p2.coefficient, p2.exponent)
            p2 = p2.get_next()
        if result_head is None:
            result_head = Term(0, 0)

        # Reconstruct the polynomial from the merged linked list.
        temp = []
        current = result_head
        while current is not None:
            temp.append((current.coefficient, current.exponent))
            current = current.get_next()
        return Polynomial(temp)
