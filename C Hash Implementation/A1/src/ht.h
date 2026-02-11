
/* ht.h
 * 
 * Public interface to the hashtable data structure.
 *
 * Please do not modify any code in this file!  We will be testing your code
 * under the assumption that the public interface matches this interface.
 *
 * Author: <TODO: Dele Osuma>
 * Lab instructor: <TODO: Your lab instructor's name here>
 * Lecture instructor: <TODO: Your lecture instructor's name here>
 */

#ifndef _HT_H_
#define _HT_H_

#define START_SIZE 7

/* With this incomplete declaration, other compilation units will be aware of 
 * the existence of a structure named `ht` but will not know anything about its
 * struct members, its size, etc.  The actual definition will be written by you
 * and will reside in a different header file, which will not be included by 
 * external users of the hash table.  In this way, we are able to ensure the
 * property of _information hiding_ behind an _interface boundary_.
 */
struct ht;


/* As we discussed in lecture, typedefs are not as commonly used as one might
 * think, but two good reasons to use them are:
 * a) simplifying a type by removing the `struct` portion of the type;
 * b) abstracting away the pointer portion of the type, if users of the type
 * only pass the pointer around as a "handle" and never access its contents.
 *
 * We have done so here.  In other words, the external users of the hash table
 * data type may forget that under the hood, it is a pointer to a structure. 
 */
typedef struct ht* hashtable;

/******************************** Functions ***********************************/

/* Notice that we have prefaced all the function names with `ht_`.  In languages
 * that support modules, packages, or namespaces, this is unnecessary.  However,
 * giving a common prefix to related functions helps in languages like C that do
 * not support namespacing. */


/* Allocates memory for, and returns an empty hashtable.  
 *
 * Returns either a valid hashtable (the address of `struct ht`), or NULL if
 * a failure to allocate occurred.
 *
 * As a result, caller will be responsible for checking whether an allocation
 * error occurred, and calling `ht_free()` on this hashtable when it is done
 * with the data structure.
 */
hashtable ht_create(void);


/* Deallocates all memory used by the hashtable's internal data structures and
 * the hashtable itself.  If the hashtable is the NULL pointer, then in the
 * style of `free()`, this function is a no-op.  After returning, the hashtable
 * must not be used, since it now points to freed memory, and should probably
 * be assigned the value NULL for safety. */
void ht_free(hashtable ht);


/* Associates the supplied key with the supplied value in the hash table.
 * If the key is already present in the hash table, it is associated to 
 * the new value.
 *
 * Additionally, a _resizing_ operation may occur during an insertion.  This
 * happens when the hash table has gotten "too full" for the number of elements
 * in the table, and the table must be resized.
 */
void ht_insert(hashtable ht, char *key, char *value);


/* Finds the value associated with a given key.  Returns NULL if no such
 * value exists.   Ownership of the key's value is retained by the hash
 * table.
 *
 * Lookup needs to be O(1) in the number of elements in the hashtable.
 */
void * ht_lookup(const hashtable ht, const char *key);

/* Removes the given key from the hashtable.
 *
 * If the key is not in the hashtable, this is a no-op.  Otherwise, the memory
 * held by `key` and its value are freed, and any reference to key is removed
 * from the hashtable's internal data structures.
 */
void ht_remove(hashtable ht, const char *key);


/* This debugging function prints on standard out the keys in the hashtable
 * along side the null entries. For instance, if `ht` is of size 7 and contains
 * 3 elements (Edmonon, Calgary, Montreal) then the prinout might look like this:
 * 
 *  Calgary
 *  NULL
 *  NULL
 *  Edmonton
 *  Montreal
 *  NULL
 *  NULL
 * 
 * You should make use of this to ensure that your hash function is doing a
 * reasonable job spreading keys evenly across the hash table and no clustering
 * is occurring.
 */
void ht_print_dist(const hashtable ht);


/* This function prints out the k,v pairs in the hashtable in the following 
 * format:
 *
 * Key
 * Value
 * 
 * Key
 * Value
 * 
 */
void ht_print(const hashtable ht);


/* This function finds a specific value in a hashtable 

it returns the index in an integer and link the value to the pointer *value 
*/
/*int ht_lookup(hashtable table, const char *key, char *value); */


#endif
