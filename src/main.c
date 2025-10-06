
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

-
typedef struct {
    char *key;
    long count;
} item_t;

typedef struct {
    item_t *items;
    size_t used;
    size_t size;
} map_t;

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
    for (size_t i = 0; i < m->used; i++) free(m->items[i].key);
    free(m->items);
}

/
void normalize_and_split(char *lyrics, map_t *word_map) {
    char *token = strtok(lyrics, " ,.!?;:\"()\r\n\t");
    while (token) {
        for (char *p = token; *p; p++) *p = tolower(*p);
        map_add(word_map, token);
        token = strtok(NULL, " ,.!?;:\"()\r\n\t");
    }
}


int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc < 2) {
        if (rank == 0) fprintf(stderr, "Uso: %s dataset.csv\n", argv[0]);
        MPI_Finalize();
        return 1;
    }

    const char *csv_path = argv[1];
    FILE *f = fopen(csv_path, "r");
    if (!f) {
        perror("Erro ao abrir CSV");
        MPI_Finalize();
        return 1;
    }

    map_t word_map, artist_map;
    map_init(&word_map);
    map_init(&artist_map);

    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    long line_idx = 0;

    
    read = getline(&line, &len, f);

    while ((read = getline(&line, &len, f)) != -1) {
        if ((line_idx % size) != rank) { line_idx++; continue; }

        char *dup = strdup(line);
        char *p1 = strchr(dup, ',');
        if (!p1) { free(dup); line_idx++; continue; }
        *p1 = '\0';
        char *p2 = strchr(p1 + 1, ',');
        if (!p2) { free(dup); line_idx++; continue; }
        *p2 = '\0';

        char *track_id = dup;
        char *artist = p1 + 1;
        char *lyrics = p2 + 1;

        
        char *nl = strchr(lyrics, '\n');
        if (nl) *nl = '\0';

        // Remove espaços extras
        while (*artist && isspace((unsigned char)*artist)) artist++;

        if (strlen(artist) > 0) map_add(&artist_map, artist);
        if (strlen(lyrics) > 0) normalize_and_split(lyrics, &word_map);

        free(dup);
        line_idx++;
    }

    free(line);
    fclose(f);

    
    char fnamew[256], fnamea[256];
    snprintf(fnamew, sizeof(fnamew), "partial_words_%d.txt", rank);
    snprintf(fnamea, sizeof(fnamea), "partial_artists_%d.txt", rank);

    FILE *fw = fopen(fnamew, "w");
    for (size_t i = 0; i < word_map.used; i++)
        fprintf(fw, "%s\t%ld\n", word_map.items[i].key, word_map.items[i].count);
    fclose(fw);

    FILE *fa = fopen(fnamea, "w");
    for (size_t i = 0; i < artist_map.used; i++)
        fprintf(fa, "%s\t%ld\n", artist_map.items[i].key, artist_map.items[i].count);
    fclose(fa);

    map_free(&word_map);
    map_free(&artist_map);

    MPI_Barrier(MPI_COMM_WORLD);
    if (rank == 0) printf("Partials gerados. Rode `python/reducer.py` para agregar resultados.\n");

    MPI_Finalize();
    return 0;
}
