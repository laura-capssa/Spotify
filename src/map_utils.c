#include "map_utils.h"

void map_init(map_t *m) {
    m->used = 0;
    m->size = 128;
    m->items = malloc(m->size * sizeof(item_t));
}

void map_add(map_t *m, const char *key) {
    for (size_t i = 0; i < m->used; i++) {
        if (strcmp(m->items[i].key, key) == 0) {
            m->items[i].count++;
            return;
        }
    }
    
    if (m->used == m->size) {
        m->size *= 2;
        m->items = realloc(m->items, m->size * sizeof(item_t));
    }
    
    m->items[m->used].key = strdup(key);
    m->items[m->used].count = 1;
    m->used++;
}

void map_free(map_t *m) {
    for (size_t i = 0; i < m->used; i++) {
        free(m->items[i].key);
    }
    free(m->items);
}

void normalize_and_split(const char *text, map_t *word_map) {
    char *copy = strdup(text);
    char *token = strtok(copy, " \t\n\r.,!?;:\"()[]{}");
    
    while (token != NULL) {
        if (strlen(token) > 0) {
            for (char *p = token; *p; p++) *p = tolower(*p);
            map_add(word_map, token);
        }
        token = strtok(NULL, " \t\n\r.,!?;:\"()[]{}");
    }
    
    free(copy);
}