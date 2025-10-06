#ifndef MAP_UTILS_H
#define MAP_UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    char *key;
    long count;
} item_t;

typedef struct {
    item_t *items;
    size_t used;
    size_t size;
} map_t;

void map_init(map_t *m);
void map_add(map_t *m, const char *key);
void map_free(map_t *m);
void normalize_and_split(const char *text, map_t *word_map);

#endif