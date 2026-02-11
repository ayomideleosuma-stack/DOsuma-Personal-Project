import numpy as np

class Table:
    """
     A hash table implemented using open addressing with linear probing.
    
    supports insertion, lookup, deletion, and automatic resizing when the load 
    factor (number of entries / table size) reaches 2/3. Uses a NumPy array as the 
    storage and Python's built-in hash() for hashing.
    
    Author: Dele Osuma
    """
    
    def __init__(self, capacity=100):
        """
        Initializes the Table.
        
        Parameters:
            capacity (int): The expected number of entries. The actual table size will be the next
                            prime number at least 1.5 times this capacity.
        """
        self.capacity = capacity
        self.size = self._next_prime(int(1.5 * capacity))
        self.table = np.full(self.size, None, dtype=object)
        self.count = 0
        self._deleted = object()  # Marker for deleted entries

    def isprime(self, value):
        """
        Checks if a given number is prime.
        
        Parameters:
            value (int): The number to check.
        
        Returns:
            bool: True if value is prime, False otherwise.
        """
        if value <= 1:
            return False
        for i in range(2, int(value ** 0.5) + 1):
            if value % i == 0:
                return False
        return True

    def _next_prime(self, n):
        """
        Finds and returns the next prime number greater than or equal to n.
        
        Parameters:
            n (int): The starting number.
        
        Returns:
            int: The next prime number.
        """
        while not self.isprime(n):
            n += 1
        return n

    def _hash(self, key):
        """
        Computes the hash index for a key.
        
        Parameters:
            key: The key to hash.
        
        Returns:
            int: The hash index within the table.
        """
        return hash(key) % self.size

    def add(self, key, value):
        """
        Adds a key-value pair to the table. If the key already exists, updates its value.
        If the load factor reaches 2/3 or above, resizes the table.
        
        Parameters:
            key: The key to add.
            value: The value associated with the key.
        """
        idx = self._hash(key)
        start_idx = idx
        first_deleted_index = None
        
        while True:
            entry = self.table[idx]
            if entry is None:
                # Empty slot found.
                if first_deleted_index is not None:
                    idx = first_deleted_index
                self.table[idx] = (key, value)
                self.count += 1
                break
            elif entry is self._deleted:
                # the first deleted slot encountered.
                if first_deleted_index is None:
                    first_deleted_index = idx
            else:
                k, v = entry
                if k == key:
                    # Key already exists, update its value.
                    self.table[idx] = (key, value)
                    return
            idx = (idx + 1) % self.size
            if idx == start_idx:
                raise Exception("Table is full, unexpected condition!")
        
        if self.load() >= 2/3:
            self._resize()

    def get(self, key):
        """
        Retrieves the value associated with the given key.
        
        Parameters:
            key: The key to search for.
        
        Returns:
            The value associated with the key.
        
        Raises:
            KeyError: If the key is not found.
        """
        idx = self._hash(key)
        start_idx = idx
        
        while True:
            entry = self.table[idx]
            if entry is None:
                raise KeyError(key)
            elif entry is not self._deleted:
                k, v = entry
                if k == key:
                    return v
            idx = (idx + 1) % self.size
            if idx == start_idx:
                break
        raise KeyError(key)

    def remove(self, key):
        """
        Removes the key (and its associated value) from the table.
        
        Parameters:
            key: The key to remove.
        
        Raises:
            KeyError: If the key is not found.
        """
        idx = self._hash(key)
        start_idx = idx
        
        while True:
            entry = self.table[idx]
            if entry is None:
                raise KeyError(key)
            elif entry is not self._deleted:
                k, v = entry
                if k == key:
                    self.table[idx] = self._deleted
                    self.count -= 1
                    return
            idx = (idx + 1) % self.size
            if idx == start_idx:
                break
        raise KeyError(key)

    def keys(self):
        """
        Returns a set of all keys in the table.
        
        Returns:
            set: A set containing all the keys.
        """
        result = set()
        for entry in self.table:
            if entry is not None and entry is not self._deleted:
                result.add(entry[0])
        return result

    def load(self):
        """
        Returns the load factor of the table.
        
        Returns:
            float: The load factor (number of entries / table size).
        """
        return self.count / self.size

    def __str__(self):
        """
        Returns a string representation of all key-value pairs in the table.
        Format: {<key: value>, <key: value>, ...}
        
        Returns:
            str: String representation of the table.
        """
        items = []
        for entry in self.table:
            if entry is not None and entry is not self._deleted:
                items.append(f"<{entry[0]}: {entry[1]}>")
        return "{" + ", ".join(items) + "}"

    def __len__(self):
        """
        Returns the number of key-value pairs in the table.
        
        Returns:
            int: The number of entries.
        """
        return self.count

    def _show_entries(self):
        """
        Shows all entries in the table, including empty slots and deleted markers.
        """
        for idx, entry in enumerate(self.table):
            if entry is None:
                print(f"Index {idx}: None")
            elif entry is self._deleted:
                print(f"Index {idx}: _deleted")
            else:
                print(f"Index {idx}: {entry}")

    def _resize(self):
        """
        Resizes the table to a new size (a prime number roughly double the current size)
        and rehashes all valid entries.
        """
        old_table = self.table
        old_size = self.size
        self.size = self._next_prime(self.size * 2)
        self.table = np.full(self.size, None, dtype=object)
        old_count = self.count
        self.count = 0
        
        for entry in old_table:
            if entry is not None and entry is not self._deleted:
                key, value = entry
                self.add(key, value)
        # After rehashing, count should be the same.
        assert self.count == old_count

    