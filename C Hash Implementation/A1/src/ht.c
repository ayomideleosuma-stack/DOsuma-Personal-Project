#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "ht.h" /* public api */
#include "ht_impl.h" /*  */

unsigned long ht_hash_djb2(const char *s) {
	unsigned long h = 5381;
	int c;
	while ((c = (unsigned char)*s++)){
		h = h * 33 + c ;
}
	return h;
}

/* primes for table size */
static int ht_abs(int x) {return x < 0 ? -x : x;}

int ht_is_prime(int n){
	if (n < 2) return 0;
	if (n % 2 ==0) return n == 2;
	for (int d = 3; d * d <= n; d += 2)
		if (n % d == 0) return 0;
	return 1;
}

int ht_next_prime(int n){
	if (n <= 2) return 2;
	if (n % 2 == 0) n++;
	while (!ht_is_prime(n)) n+= 2;
	return n;
}

/* division method */
int ht_index_for(const char *key, int table_size){
	unsigned long h = ht_hash_djb2(key);
	return (int)(h % (unsigned long)table_size);
}

/* allocation helpers */ 
static void ht_init_entries(struct ht *t, int size){
	(*t).size = size;
	(*t).count = 0;
	(*t).tombs = 0;
	(*t).entries = (ht_entry*)calloc(size, sizeof(ht_entry));
	/* calloc : zero default == SLOT_EMPTY */
	}
/**
 *@brief Allocate/Initialize a new hash table
 * The table is created with a size of START_SIZE
 * @return A new hastbale or NULL
 * */
hashtable ht_create(void){
	struct ht *t = (struct ht*)malloc(sizeof(struct ht));
	if (!t) return NULL;
	ht_init_entries(t, START_SIZE); /* start size from ht.h */
	return t;
}

/* free */
static void ht_free_entry(ht_entry *e){
	if ((*e).state == SLOT_OCCUPIED){
		free((*e).key);
		free((*e).value);
	}
	(*e).key = NULL;
	(*e).value = NULL;
	(*e).state = SLOT_EMPTY;
}

/* free the whole table(public) */
/** 
 * @brief Free all memory associated with the hash table
 * this function frees all key/value strings stored in the table, the internal array, and the table struct
 * if @p ht is NULL, the function does not do anything 
 *
 * @param ht the Hashtable to destory
 * */
void ht_free(hashtable ht){
	if (!ht) return;
	for (int i = 0; i < (*ht).size; ++i){
		if ((*ht).entries[i].state == SLOT_OCCUPIED){
			free((*ht).entries[i].key);
			free((*ht).entries[i].value);
		}
	}
	free((*ht).entries);
	free(ht);

	/* resizing */ 
}
static double ht_load_factor(const struct ht *t){
	return ((*t).size == 0) ? 0.0 : ((double)(*t).count / (double)(*t).size);
	}

	/* reinsert utility*/
static void ht_put_into(struct ht *t, char *k, char *v) {
    int idx = ht_index_for(k, (*t).size);
    int first_tomb = -1;

    for (;;) {
        ht_entry *e = (*t).entries + idx;

        if ((*e).state == SLOT_EMPTY) {
            int target = (first_tomb >= 0) ? first_tomb : idx;
            ht_entry *dst = (*t).entries + target;
            (*dst).key = k;
            (*dst).value = v;
            (*dst).state = SLOT_OCCUPIED;
            (*t).count++;
            if (first_tomb >= 0) (*t).tombs--;/* used tombstone */
            return;
        } else if ((*e).state == SLOT_TOMBSTONE) {
            if (first_tomb < 0) first_tomb = idx;
        } else { /* OCCUPIED */
            if (strcmp((*e).key, k) == 0) {
		    /* replace existing value */
                free((*e).value);
                (*e).value = v;
                free(k);
                return;
            }
        }
        idx = (idx + 1) % (*t).size;
    }
}

void ht_resize(struct ht *old, int new_size) {
    new_size = ht_next_prime(new_size); /* (DIVISION METHOD) keeping prime sizes*/
    ht_entry *old_entries = (*old).entries;
    int old_size = (*old).size;

    (*old).entries = (ht_entry*)calloc(new_size, sizeof(ht_entry));
    (*old).size = new_size;
    (*old).count = 0;
    (*old).tombs = 0;

    for (int i = 0; i < old_size; ++i) {
        ht_entry *e = old_entries + i;
        if ((*e).state == SLOT_OCCUPIED) { /* move strings as is*/
            ht_put_into(old, (*e).key, (*e).value);
        }
    }
    free(old_entries);
}
/* ensure capacity before insert */
static void ht_maybe_grow(struct ht *t) {
	/* grow if over 2/3*/
    if (ht_load_factor(t) > (2.0 / 3.0) || (*t).tombs > (*t).size / 3) {
        ht_resize(t, (*t).size * 2);
    }
}
/* public insert */
/** 
 * @brief Insert or update a key/value pair in the hash table
 * if the key is not present, it is inserted with the given value
 * if the key already exists, its old value is freed and replaced
 * with the new value. The table grows as needed
 * @param ht the Hashtable to insert the key
 * @param key Null-terminated key string
 * @param value Null-terminated value string
 * */
void ht_insert(hashtable ht, char *key, char *value) {
    assert(ht);
    ht_maybe_grow(ht);

    char *kdup = strdup(key);
    char *vdup = strdup(value);
    if (!kdup || !vdup) {
        free(kdup);
        free(vdup);
        return;
    }

    int idx = ht_index_for(kdup, (*ht).size);
    int first_tomb = -1;

    for (;;) {
        ht_entry *e = (*ht).entries + idx;

        if ((*e).state == SLOT_EMPTY) {
            int target = (first_tomb >= 0) ? first_tomb : idx;
            ht_entry *dst = (*ht).entries + target;
            (*dst).key = kdup;
            (*dst).value = vdup;
            (*dst).state = SLOT_OCCUPIED;
            (*ht).count++;
            if (first_tomb >= 0) (*ht).tombs--;
            return;
        } else if ((*e).state == SLOT_TOMBSTONE) {
            if (first_tomb < 0) first_tomb = idx;
        } else { /*OCCUPIED*/
            if (strcmp((*e).key, kdup) == 0) {
		    /* key exist replace value*/
                free((*e).value);
                (*e).value = vdup;
                free(kdup);
                return;
            }
        }
        idx = (idx + 1) % (*ht).size;
    }
}

/*Oublic Lookup (return pointer)*/
/**
 * @brief Look up a value by key in the hash table
 *
 * @param ht the Hashtable to search
 * @param key NULL-Terminated key string
 * @return A pointer to the stored value if found or NULL
 * */
void * ht_lookup(const hashtable ht, const char *key) {
    if (!ht || !key) return NULL;
    int idx = ht_index_for(key, (*ht).size);

    for (;;) {
        ht_entry *e = (*ht).entries + idx;
        if ((*e).state == SLOT_EMPTY) return NULL;
        if ((*e).state == SLOT_OCCUPIED && strcmp((*e).key, key) == 0) {
            return (*e).value; /*found*/
        }
        idx = (idx + 1) % (*ht).size;
    }
}
/*public remove*/
/** 
 * @brief remove a key and its associated value from the hash table
 * if key is present, its key and value strings are freed. 
 * Slot is marked as tombstone so probing works
 * If the key is not present, the function doesn't do anything
 *
 * @param ht the hashtable to modify
 * @param key Null-terminated key string to remove*/
void ht_remove(hashtable ht, const char *key) {
    if (!ht || !key) return;
    int idx = ht_index_for(key, (*ht).size);

    for (;;) {
        ht_entry *e = (*ht).entries + idx;
        if ((*e).state == SLOT_EMPTY) return;
        if ((*e).state == SLOT_OCCUPIED && strcmp((*e).key, key) == 0) {
            free((*e).key);
            free((*e).value);
            (*e).key = NULL;
            (*e).value = NULL;
            (*e).state = SLOT_TOMBSTONE;
            (*ht).count--;
            (*ht).tombs++;
            return;
        }
        idx = (idx + 1) % (*ht).size;
    }
}

/*  Debug Printers*/
/** @brief Print the distribution of keys and NULLS in the table
 *
 * for each bucket, prints either the key or NULL
 *
 * @param ht the hashtable to inspect
 * */
void ht_print_dist(const hashtable ht) {
    if (!ht) return;
    for (int i = 0; i < (*ht).size; ++i) {
        ht_entry *e = (*ht).entries + i;
        if ((*e).state == SLOT_OCCUPIED) {
            printf("%s\n", (*e).key);
        } else {
            printf("NULL\n");
        }
    }
}
/** 
 *
 * @brief Print all key/value pairs in the table
 *
 * each key is printed on one line, followed by its value on the next line, then a blank line
 *
 * @param ht the Hashtable to inspect
 * */
void ht_print(const hashtable ht) {
    if (!ht) return;
    for (int i = 0; i < (*ht).size; ++i) {
        ht_entry *e = (*ht).entries + i;
        if ((*e).state == SLOT_OCCUPIED) {
            printf("%s\n%s\n\n", (*e).key, (*e).value);
        }
    }
}

