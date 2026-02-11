"""
Name: [Dele Osuma]

implements two recursive functions:
    - reorder(list_of_letters)
    - is_alternating(numbers)
"""

def reorder(list_of_letters):
    """
    Recursively reorders the list so that all vowels precede all consonants.
(a new list is returned).
    

      - If the list is already ordered,
        return a copy of it.
      - Otherwise, find the leftmost consonant that has at least one vowel later
        in the list and the rightmost vowel that occurs after that consonant.
        Swap these two elements and recursively call reorder on the new list.
    
    e.g     Input:  ['j', 'o', 'g', 'o', 'l', 'i', 's', 'b', 'p', 'a']
       Expected Output: ['a', 'o', 'i', 'o', 'l', 'g', 's', 'b', 'p', 'j']
    """
    vowels = "AEIOUaeiou"
    
    def is_ordered(l):
        # Returns True if l is arranged so that no vowel occurs after a consonant.
        first_consonant = None
        for i, ch in enumerate(l):
            if ch not in vowels:
                first_consonant = i
                break
        if first_consonant is None:
            return True  # All are vowels.
        # Once the first consonant appears, no vowel should appear later.
        for ch in l[first_consonant:]:
            if ch in vowels:
                return False
        return True

    # Base: if already ordered, return a copy.
    if is_ordered(list_of_letters):
        return list_of_letters[:]
    
    # Otherwise, find the leftmost consonant that has a vowel later.
    left = None
    for i in range(len(list_of_letters)):
        if list_of_letters[i] not in vowels and any(ch in vowels for ch in list_of_letters[i+1:]):
            left = i
            break

    # And find the rightmost vowel that occurs after that index.
    right = None
    if left is not None:
        for j in range(len(list_of_letters) - 1, left, -1):
            if list_of_letters[j] in vowels:
                right = j
                break

    # Swap the two elements.
    new_list = list_of_letters[:]
    new_list[left], new_list[right] = new_list[right], new_list[left]
    # Recursively reorder the new list.
    return reorder(new_list)


def is_alternating(numbers):
    """
    Recursively checks whether the string numbers (which should consist only of '0's
    and '1's) has alternating characters.
    
    Returns:
       True if every adjacent pair of characters is different (and the string has length >= 2),
       False otherwise.
       
    Examples:
       is_alternating('01')         -> True
       is_alternating('010101010')   -> True
       is_alternating('0110101010')  -> False
       is_alternating('')            -> False
       is_alternating('0')           -> False
    """
    # For strings of length 0 or 1, return False.
    if len(numbers) < 2:
        return False
    # Base case for exactly 2 characters.
    if len(numbers) == 2:
        return numbers[0] != numbers[1]
    # If the first two characters are the same, it's not alternating.
    if numbers[0] == numbers[1]:
        return False
    # Recurse on the substring starting at index 1.
    return is_alternating(numbers[1:])


