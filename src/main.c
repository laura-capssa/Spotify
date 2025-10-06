#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "map_utils.h"

#define MAX_LINE_LENGTH 10000

// Lista de palavras comuns que NÃO são artistas
const char *common_words[] = {
    "oh", "yeah", "no", "hey", "well", "ooh", "yes", "baby", "la", 
    "whoa", "woo", "ha", "hey", "hello", "goodbye", "okay", "alright",
    "come", "go", "stop", "wait", "please", "thank", "sorry", NULL
};

int is_common_word(const char *word) {
    for (int i = 0; common_words[i] != NULL; i++) {
        if (strcasecmp(word, common_words[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int is_valid_artist(const char *artist) {
    if (!artist || strlen(artist) == 0) return 0;
    
    // Se for uma palavra muito comum, provavelmente não é artista
    if (is_common_word(artist)) return 0;
    
    // Se tem menos de 2 caracteres, não é artista
    if (strlen(artist) < 2) return 0;
    
    // Se é apenas números, não é artista
    int all_digits = 1;
    for (const char *p = artist; *p; p++) {
        if (!isdigit(*p)) {
            all_digits = 0;
            break;
        }
    }
    if (all_digits) return 0;
    
    return 1;
}

int main(int argc, char *argv[]) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc != 2) {
        if (rank == 0) {
            printf("Uso: %s <arquivo_csv>\n", argv[0]);
        }
        MPI_Finalize();
        return 1;
    }

    map_t word_map, artist_map;
    map_init(&word_map);
    map_init(&artist_map);

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        printf("Processo %d: Erro ao abrir arquivo %s\n", rank, argv[1]);
        MPI_Finalize();
        return 1;
    }

    char line[MAX_LINE_LENGTH];
    long local_line_count = 0;
    
    // Pular cabeçalho
    if (rank == 0) {
        fgets(line, sizeof(line), file);
    }

    while (fgets(line, sizeof(line), file)) {
        local_line_count++;
        
        if (local_line_count % size == rank) {
            char *dup = strdup(line);
            
            // Encontrar a primeira vírgula (artista)
            char *first_comma = strchr(dup, ',');
            if (first_comma) {
                *first_comma = '\0';
                char *artist = dup;
                
                // Encontrar o início da letra (terceira vírgula)
                char *lyrics_start = first_comma + 1;
                for (int i = 0; i < 2; i++) {
                    lyrics_start = strchr(lyrics_start, ',');
                    if (!lyrics_start) break;
                    lyrics_start++;
                }
                
                if (lyrics_start) {
                    // Remover aspas do artista se existirem
                    if (artist[0] == '"' && artist[strlen(artist)-1] == '"') {
                        memmove(artist, artist + 1, strlen(artist));
                        artist[strlen(artist)-1] = '\0';
                    }
                    
                    // Contar artista APENAS se for válido
                    if (strlen(artist) > 0 && is_valid_artist(artist)) {
                        map_add(&artist_map, artist);
                    }
                    
                    // Contar palavras da letra
                    if (strlen(lyrics_start) > 0) {
                        normalize_and_split(lyrics_start, &word_map);
                    }
                }
            }
            
            free(dup);
        }
    }
    
    fclose(file);

    // Escrever resultados parciais
    char word_filename[50], artist_filename[50];
    sprintf(word_filename, "partial_words_%d.txt", rank);
    sprintf(artist_filename, "partial_artists_%d.txt", rank);
    
    FILE *fw = fopen(word_filename, "w");
    FILE *fa = fopen(artist_filename, "w");
    
    for (size_t i = 0; i < word_map.used; i++) {
        fprintf(fw, "%s\t%ld\n", word_map.items[i].key, word_map.items[i].count);
    }
    
    for (size_t i = 0; i < artist_map.used; i++) {
        fprintf(fa, "%s\t%ld\n", artist_map.items[i].key, artist_map.items[i].count);
    }
    
    fclose(fw);
    fclose(fa);

    map_free(&word_map);
    map_free(&artist_map);

    if (rank == 0) {
        printf("Processamento concluído. Resultados parciais gerados.\n");
    }

    MPI_Finalize();
    return 0;
}
