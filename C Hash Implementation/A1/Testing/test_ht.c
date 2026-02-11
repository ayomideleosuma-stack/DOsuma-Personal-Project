#include <CUnit/CUnit.h>
#include <CUnit/Basic.h>
#include <string.h>
#include "../ht.h"

static void test_insert_lookup_single(void) {
    hashtable t = ht_create();
    CU_ASSERT_PTR_NOT_NULL(t);

    ht_insert(t, "Edmonton", "T5J");
    char *v = (char *)ht_lookup(t, "Edmonton");
    CU_ASSERT_PTR_NOT_NULL(v);
    if (v) {
        CU_ASSERT_STRING_EQUAL(v, "T5J");
    }

    ht_free(t);
}

static void test_update_value(void) {
    hashtable t = ht_create();

    ht_insert(t, "Calgary", "T2P");
    ht_insert(t, "Calgary", "T3K");
    char *v = (char *)ht_lookup(t, "Calgary");
    CU_ASSERT_PTR_NOT_NULL(v);
    if (v) {
        CU_ASSERT_STRING_EQUAL(v, "T3K");
    }

    ht_free(t);
}

static void test_remove(void) {
    hashtable t = ht_create();

    ht_insert(t, "Montreal", "H1A");
    CU_ASSERT_PTR_NOT_NULL(ht_lookup(t, "Montreal"));

    ht_remove(t, "Montreal");
    CU_ASSERT_PTR_NULL(ht_lookup(t, "Montreal"));

    ht_free(t);
}

static void test_resize(void) {
    hashtable t = ht_create();
    char key[32], val[32];

    for (int i = 0; i < 100; ++i) {
        snprintf(key, sizeof(key), "City%d", i);
        snprintf(val, sizeof(val), "P%03d", i);
        ht_insert(t, key, val);
    }

    for (int i = 0; i < 100; ++i) {
        snprintf(key, sizeof(key), "City%d", i);
        snprintf(val, sizeof(val), "P%03d", i);
        char *v = (char *)ht_lookup(t, key);
        CU_ASSERT_PTR_NOT_NULL(v);
        if (v) {
            CU_ASSERT_STRING_EQUAL(v, val);
        }
    }

    ht_free(t);
}

int main(void) {
    if (CUE_SUCCESS != CU_initialize_registry())
        return CU_get_error();

    CU_pSuite s = CU_add_suite("ht_suite", NULL, NULL);
    if (s == NULL) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    if ((CU_add_test(s, "insert_lookup_single", test_insert_lookup_single) == NULL) ||
        (CU_add_test(s, "update_value",         test_update_value)         == NULL) ||
        (CU_add_test(s, "remove",               test_remove)               == NULL) ||
        (CU_add_test(s, "resize",               test_resize)               == NULL)) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_cleanup_registry();
    return CU_get_error();
}

