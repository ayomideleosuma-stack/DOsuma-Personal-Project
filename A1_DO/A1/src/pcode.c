#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ht.h"

static void strip_newline(char *s) {
    if (!s) return;
    int len = (int)strlen(s);
    if (len > 0 && s[len - 1] == '\n') {
        s[len - 1] = '\0';
    }
}

static void rstrip_spaces(char *s) {
    int len = (int)strlen(s);
    while (len > 0 && (s[len - 1] == ' ' || s[len - 1] == '\t')) {
        s[len - 1] = '\0';
        len--;
    }
}

static void lstrip_spaces(char **s) {
    while (**s == ' ' || **s == '\t') {
        (*s)++;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <inputfile>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (!fp) {
        perror("file");
        return 1;
    }

    hashtable table = ht_create();
    if (!table) {
        fclose(fp);
        fprintf(stderr, "Failed to create hashtable\n");
        return 1;
    }

    char line[256];

    /* load file: each line "CITY ... POSTAL" */
    while (fgets(line, sizeof(line), fp) != NULL) {
        strip_newline(line);
        if (line[0] == '\0') continue;

        char *comma = strrchr(line, ',');
        if (!comma) continue;

        *comma  = '\0';
        char *city = line;
        char *postal = comma + 1;

        rstrip_spaces(city);
        lstrip_spaces(&city);
        rstrip_spaces(postal);
        lstrip_spaces(&postal);

        if (city[0] == '\0' || postal[0] == '\0') continue;

	for (char *p = city; *p; p++)
	       	if (*p >= 'A' && *p <= 'Z') *p = *p + ('a' - 'A');

        char *existing = (char *)ht_lookup(table, city);
        if (existing) {
            char buffer[1024];
            snprintf(buffer, sizeof(buffer), "%s,%s", existing, postal);
            ht_insert(table, city, buffer);
        } else {
            ht_insert(table, city, postal);
        }
    }

    fclose(fp);

    /* query phase: read city names from stdin */
    char query[256];
    while (1) {
    	printf("Please Enter a city name: ");
    	if (!fgets(query, sizeof(query), stdin))
        	break;
        strip_newline(query);
        if (query[0] == '\0') continue;
        rstrip_spaces(query);
        char *qptr = query;
        lstrip_spaces(&qptr);
        if (qptr[0] == '\0') continue;
	for (char *p = qptr; *p; p++){
		if (*p >= 'A' && *p <= 'Z') *p = *p + ('a' - 'A');
	}
	char *codes = (char *)ht_lookup(table, qptr);
        if (codes) {
            printf("%s\n", codes);
        } else {
		printf("No record exists!\n");
        }
    }

    ht_free(table);
    return 0;
}

