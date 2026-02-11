''' 
Author: Dele Osuma

'''

import string

# Binary Search Tree class with frequency, depth, and parent tracking

class BST:
    class _Node:
        def __init__(self, value, depth, parent=None):
            # Initialize a node with a value, depth, parent, and empty children
            self._value = value
            self._count = 1
            self._depth = depth
            self._parent = parent
            self._left = None
            self._right = None

    def __init__(self):
        # Initialize the tree with an empty root and counters
        self._root = None
        self._total_words = 0
        self._distinct_words = 0

    def is_empty(self):
        # Check if the tree is empty
        return self._root is None

    def insert(self, word):
        '''
        Inserts a word into the BST. If the word already exists,
        increment its frequency. Otherwise, add a new node at the correct location.
        '''
        if self._root is None:
            # First node becomes the root
            self._root = self._Node(word, 0)
            self._distinct_words += 1
            self._total_words += 1
            return

        current = self._root
        depth = 0
        parent = None
        # Traverse to find the insertion point
        while current is not None:
            if word == current._value:
                current._count += 1
                self._total_words += 1
                return
            parent = current
            depth += 1
            if word < current._value:
                current = current._left
            else:
                current = current._right

        # Create a new node and attach to parent
        new_node = self._Node(word, depth, parent)
        if word < parent._value:
            parent._left = new_node
        else:
            parent._right = new_node
        self._distinct_words += 1
        self._total_words += 1

    def search(self, word):
        # Traverse the tree to search for a word
        current = self._root
        while current is not None:
            if word == current._value:
                print(f"For this word: {word}[{current._count}]")
                return
            elif word < current._value:
                current = current._left
            else:
                current = current._right
        print(f"{word} is not in the tree")

    def in_order(self):
        # method to trigger in-order traversal
        if self._root is None:
            print("Tree is empty")
        else:
            print("Printing the tree")
            self._in_order_recursive(self._root)

    def _in_order_recursive(self, node):
        # In-order traversal prints nodes in alphabetical order
        if node is None:
            return
        self._in_order_recursive(node._left)
        parent_val = node._parent._value if node._parent else "None"
        print(f"{node._value}[{node._count}], depth = {node._depth}, parent = {parent_val}")
        self._in_order_recursive(node._right)

    def delete(self, word):
        '''
        Deletes a word from the BST. If the word exists, it is removed,
        and a message with the count is printed. Otherwise, reports not found.
        '''
        self._root, deleted, count = self._delete_rec(self._root, word)
        if deleted:
            self._distinct_words -= 1
            self._total_words -= count
            print(f"{word} deleted, it had {count} occurrences")
        else:
            print(f"{word} is not in the tree")

    def _delete_rec(self, node, word):
        # Recursive helper for delete
        if node is None:
            return node, False, 0
        if word < node._value:
            node._left, deleted, count = self._delete_rec(node._left, word)
        elif word > node._value:
            node._right, deleted, count = self._delete_rec(node._right, word)
        else:
            count = node._count
            if node._left is None:
                return node._right, True, count
            elif node._right is None:
                return node._left, True, count
            # Replace with in-order successor
            min_larger_node = self._min_value_node(node._right)
            node._value, node._count = min_larger_node._value, min_larger_node._count
            node._right, _, _ = self._delete_rec(node._right, min_larger_node._value)
            return node, True, count
        return node, deleted, count

    def _min_value_node(self, node):
        # Get the node with the minimum value in a subtree
        current = node
        while current._left is not None:
            current = current._left
        return current

    def read_file(self, file_name):
        '''
        Reads text from a file, cleans punctuation and upper-case letters,
        then inserts words into the BST.
        '''
        try:
            file = open(file_name, 'r')
        except:
            print("File not found")
            return
        while True:
            line = file.readline()
            if line == '':
                break
            cleaned = self._clean_line(line)
            words = cleaned.split()
            for word in words:
                if word != '':
                    self.insert(word)
        file.close()

    def _clean_line(self, line):
        # Clean punctuation (except _ and ') and convert to lowercase
        line = line.lower()
        cleaned = ''
        for ch in line:
            if ch in string.punctuation and ch != '_' and ch != "'":
                cleaned += ' '
            else:
                cleaned += ch
        return cleaned

    def levelprint(self):
        '''Prints tree level by level from deepest to root, right to left in each level.'''
        if self._root is None:
            print("Tree is empty")
            return

        print("Level print of the tree")

        queue = [self._root]
        levels = {}

        # Grouping nodes by their depth using level-order traversal
        while queue:
            node = queue.pop(0)
            depth = node._depth
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)

            if node._left:
                queue.append(node._left)
            if node._right:
                queue.append(node._right)

        # Print levels from deepest to root, right to left
        for depth in sorted(levels.keys())[::-1]:
            values = sorted([f"{node._value}[{node._count}]" for node in levels[depth]])[::-1]
            print(f"Depth {depth}: {', '.join(values)}")

    def first(self):
        # Print the smallest word in the tree
        if self._root is None:
            print("Tree is empty")
            return
        current = self._root
        while current._left is not None:
            current = current._left
        print(f"The first word is {current._value}")

    def last(self):
        # Print the largest word in the tree
        if self._root is None:
            print("Tree is empty")
            return
        current = self._root
        while current._right is not None:
            current = current._right
        print(f"The last word is {current._value}")

    def most(self):
        # Print the most frequent word(s) in the tree
        if self._root is None:
            print("Tree is empty")
            return
        max_count, result = [0], []
        self._find_most(self._root, max_count, result)
        print(f"The most occurrences is  {max_count[0]}")
        for word in sorted(result):
            print(f"{word}, count =  {max_count[0]}")

    def _find_most(self, node, max_count, result):
        # Helper for finding the most frequent word(s)
        if node is None:
            return
        if node._count > max_count[0]:
            max_count[0] = node._count
            result.clear()
            result.append(node._value)
        elif node._count == max_count[0]:
            result.append(node._value)
        self._find_most(node._left, max_count, result)
        self._find_most(node._right, max_count, result)

    def summary(self):
        '''
        Prints a summary of the BST: height, total word count,
        number of distinct words, first and last words alphabetically.
        '''
        if self._root is None:
            print("Tree is empty")
            return
        height = self._calculate_height(self._root)
        print("** Tree Statistics **")
        print(f"\tHeight of tree: {height}")
        print(f"\tTotal words: {self._total_words}, Distinct words: {self._distinct_words}")
        self.first()
        self.last()

    def _calculate_height(self, node):
        # Compute height of the tree recursively
        if node is None:
            return -1
        return 1 + max(self._calculate_height(node._left), self._calculate_height(node._right))


def main():
    '''
    Main function for processing user commands.
    Supported commands: read, print, search, delete, first, last,
    most, summary, levelprint, and quit.
    '''
    tree = BST()
    while True:
        try:
            user_input = input().strip()
        except:
            break
        if user_input == 'quit':
            print("** BST Program Finished **")
            break
        elif user_input.startswith("read "):
            filename = user_input[5:].strip()
            tree.read_file(filename)
        elif user_input == "print":
            tree.in_order()
        elif user_input.startswith("search "):
            word = user_input[7:].strip().lower()
            tree.search(word)
        elif user_input.startswith("delete "):
            word = user_input[7:].strip().lower()
            tree.delete(word)
        elif user_input == "first":
            tree.first()
        elif user_input == "last":
            tree.last()
        elif user_input == "most":
            tree.most()
        elif user_input == "summary":
            tree.summary()
        elif user_input == "levelprint":
            tree.levelprint()
        else:
            print("Unknown command")


if __name__ == '__main__':
    main()

