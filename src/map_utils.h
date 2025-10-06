#ifndef MAP_UTILS_H
#define MAP_UTILS_H


typedef struct {
char *key;
long count;
} kv_pair;


typedef struct {
kv_pair *items;
size_t used;
size_t cap;
} map_t;


void map_init(map_t *m);
void map_free(map_t *m);
void map_add(map_t *m, const char *key);
void map_add_count(map_t *m, const char *key, long c);
int map_find_idx(map_t *m, const char *key);
void map_sort(map_t *m); // sort by key (lexicographic) or by count (if needed)


#endif