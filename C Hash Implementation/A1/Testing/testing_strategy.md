# CMPT 201 – Assignment 1
## Testing Strategy Document
## Student: Dele Osuma

## Purpose of Testing

The goal of testing is to verify that the hash table meets the
requirements described in the assignment specification. All tests are automated
using the CUnit framework.

Testing is performed on the four required public API functions:

- `ht_insert()`
- `ht_lookup()`
- `ht_remove()`
- `ht_resize()`

The tests make sure that it is correct before the hash table is used inside `pcode`.

## Testing Framework

All tests are implemented using **CUnit Basic** mode and can be executed with:

## make test_ht
## ./test_ht

Each test uses `CU_ASSERT` checks to verify expected behavior.

No manual checking is required.

### Test Case 1 – Insert and Lookup
Verifies that inserting one key/value pair allows a correct lookup.

### Test Case 2 – Update Existing Key
Ensures that inserting the same key twice updates the value and does not produce duplicates.

### Test Case 3 – Remove
Ensures that removing a key makes future lookups return NULL.

### Test Case 4 – Resize
Adds 100+ key/value pairs to force resizing and verifies that all values are still correct afterward.

All tests also pass under Valgrind:
