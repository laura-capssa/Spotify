#!/usr/bin/env python3
import sys
from collections import defaultdict
import os
import glob

def combine_files(pattern):
    combined = defaultdict(int)
    
    for filename in glob.glob(pattern):
        print(f"Processando {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and '\t' in line:
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            key = parts[0].strip()
                            count_str = parts[1].strip()
                            try:
                                count = int(count_str)
                                combined[key] += count
                            except ValueError:
                                print(f"  Aviso: Valor não numérico na linha {line_num}: '{count_str}'")
                        else:
                            print(f"  Aviso: Formato inválido na linha {line_num}: {line}")
                    elif line and line.strip():  # Linha não vazia mas sem tab
                        print(f"  Aviso: Ignorando linha {line_num} sem tab: {line}")
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")
    
    return combined

def main():
    print("Combinando contagem de palavras...")
    word_counts = combine_files('partial_words_*.txt')
    
    print("Combinando contagem de artistas...")
    artist_counts = combine_files('partial_artists_*.txt')
    
    # Salvar resultados finais
    print("Salvando resultados...")
    with open('total_word_counts.txt', 'w', encoding='utf-8') as f:
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:100]:
            f.write(f"{word}\t{count}\n")
    
    with open('total_artist_counts.txt', 'w', encoding='utf-8') as f:
        for artist, count in sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:50]:
            f.write(f"{artist}\t{count}\n")
    
    # Estatísticas
    print(f"\n=== ESTATÍSTICAS ===")
    print(f"Total de palavras únicas: {len(word_counts)}")
    print(f"Total de artistas únicos: {len(artist_counts)}")
    
    print("\n--- TOP 10 ARTISTAS ---")
    top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (artist, count) in enumerate(top_artists, 1):
        print(f"{i:2d}. {artist}: {count} músicas")
    
    print("\n--- TOP 10 PALAVRAS ---")
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (word, count) in enumerate(top_words, 1):
        print(f"{i:2d}. {word}: {count} ocorrências")
    
    # Limpar arquivos parciais
    partial_files = glob.glob('partial_*.txt')
    for f in partial_files:
        os.remove(f)
    print(f"\nRemovidos {len(partial_files)} arquivos parciais")
    
    print("\n=== REDUÇÃO CONCLUÍDA ===")
    print("Resultados salvos em:")
    print("✓ total_word_counts.txt (top 100 palavras)")
    print("✓ total_artist_counts.txt (top 50 artistas)")

if __name__ == "__main__":
    main()