#include "map_utils.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


static char *strdup_local(const char *s) {
size_t n = strlen(s)+1;
char *d = malloc(n);
if (d) memcpy(d, s, n);
return d;
}


void map_init(map_t *m) {
m->used = 0; m->cap = 1024;
m->items = malloc(sizeof(kv_pair)*m->cap);
}


void map_free(map_t *m) {
if (!m) return;
for (size_t i=0;i<m->used;i++) free(m->items[i].key);
free(m->items);
}


int map_find_idx(map_t *m, const char *key) {
for (size_t i=0;i<m->used;i++) {
if (strcmp(m->items[i].key, key)==0) return (int)i;
}
return -1;
}


void map_add(map_t *m, const char *key) {
int idx = map_find_idx(m,key);
if (idx>=0) { m->items[idx].count += 1; return; }
if (m->used >= m->cap) {
m->cap *= 2;
m->items = realloc(m->items, sizeof(kv_pair)*m->cap);
}
m->items[m->used].key = strdup_local(key);
m->items[m->used].count = 1;
m->used++;
}


void map_add_count(map_t *m, const char *key, long c) {
int idx = map_find_idx(m,key);
if (idx>=0) { m->items[idx].count += c; return; }
if (m->used >= m->cap) {
m->cap *= 2;
m->items = realloc(m->items, sizeof(kv_pair)*m->cap);
}
m->items[m->used].key = strdup_local(key);
m->items[m->used].count = c;
m->used++;
}


int cmp_count_desc(const void *a,const void *b){
const kv_pair *A = a; const kv_pair *B = b;
if (A->count < B->count) return 1;
if (A->count > B->count) return -1;
return strcmp(A->key,B->key);
}


void map_sort(map_t *m) {
qsort(m->items, m->used, sizeof(kv_pair), cmp_count_desc);
}