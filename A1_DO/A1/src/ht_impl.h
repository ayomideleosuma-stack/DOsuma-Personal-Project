/* ht_impl.h
 *
 * For any "private"  declarations that should not be visible to the public
 * users of the hash table, but might want to be shared across various sources
 * files in the hash table implementation.
 * 
 * It is a standard convention to append "_impl" to a private implementation of
 * some public interface, so we do so here.
 *
 * Author: <TODO: your name here>
 * Lab instructor: <TODO: Your lab instructor's name here>
 * Lecture instructor: <TODO: Your lecture instructor's name here>
 */

#ifndef _HT_IMPL_H_
#define _HT_IMPL_H_

/* TODO: think of some things that should go in here! */

/*
Examples:
hashing function 
indexing function 
A function to identify whether the number is prime or not 
A function to get the following prime number for a specific number 

*/ 
#include <stdbool.h>
#define SLOT_EMPTY 0 /* linear probing*/
#define SLOT_OCCUPIED 1
#define SLOT_TOMBSTONE 2

typedef struct{
        char *key; /* null terminaed strings */
        char *value;
        int state;
} ht_entry;

struct ht{
        int size; /* # of buckets*/
        int count; /* # of occupied slots*/
        int tombs;
        ht_entry *entries;
};
/* private helpers */
unsigned long ht_hash_djb2(const char *s);
int ht_is_prime(int n);
int ht_next_prime(int n);
int ht_index_for(const char *key, int table_size); /* division method  */
void ht_resize(struct ht *t, int new_size);


#endif
