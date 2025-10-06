#!/usr/bin/env python3
import csv
import time
from collections import Counter
import sys
import os

def simulate_sentiment_analysis(text):
    """
    Analisa sentimentos baseada em palavras-chave
    """
    if not text:
        return "Neutra"
    
    text_lower = text.lower()
    
    # Palavras positivas 
    positive_words = [
        'love', 'happy', 'beautiful', 'success', 'win', 'victory', 
        'strong', 'power', 'money', 'rich', 'dream', 'hope', 'future',
        'king', 'champ', 'best', 'great', 'amazing', 'legend', 'god',
        'bless', 'peace', 'family', 'loyal', 'respect', 'honor'
    ]
    
    # Palavras negativas 
    negative_words = [
        'hate', 'kill', 'death', 'murder', 'war', 'fight', 'violence',
        'pain', 'hurt', 'suffer', 'broken', 'lost', 'alone', 'dark',
        'hell', 'devil', 'enemy', 'betray', 'lie', 'fake', 'traitor',
        'struggle', 'poor', 'ghetto', 'street', 'blood', 'tears', 'cry',
        'anger', 'mad', 'rage', 'revenge', 'jail', 'prison', 'crime'
    ]
    
    # Palavras neutras que não indicam sentimento forte
    neutral_context = [
        'rap', 'hiphop', 'mic', 'flow', 'rhyme', 'beat', 'track',
        'album', 'song', 'music', 'verse', 'hook', 'chorus'
    ]
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    neutral_context_count = sum(1 for word in neutral_context if word in text_lower)
    
    # Ajustar contagem considerando contexto neutro
    adjusted_positive = positive_count
    adjusted_negative = negative_count
    
    # Se tiver muitas palavras de contexto neutro, tende para neutro
    if neutral_context_count > 3:
        if abs(positive_count - negative_count) <= 2:
            return "Neutra"
    
    if adjusted_positive > adjusted_negative:
        return "Positiva"
    elif adjusted_negative > adjusted_positive:
        return "Negativa"
    else:
        return "Neutra"

def main():
    print("  CLASSIFICADOR DE SENTIMENTOS")
    print()
    print(" Analisando APENAS músicas do Eminem")
    print()
    
    if len(sys.argv) != 2:
        print("Uso: python3 classify_eminem.py spotify_millsongdata.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f" Arquivo não encontrado: {csv_file}")
        sys.exit(1)
    
    print(f" Analisando: {csv_file}")
    print(" Procurando músicas do Eminem...\n")
    
    sentiment_counts = Counter()
    eminem_songs = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            header = next(reader)  # Pular cabeçalho
            
            # Procurar todas as músicas do Eminem
            for row in reader:
                if len(row) >= 4:
                    artist, song, lyrics = row[0], row[1], row[3]
                    
                    # Buscar por "Eminem" no nome do artista
                    if "eminem" in artist.lower():
                        if lyrics and len(lyrics.strip()) > 50:
                            eminem_songs.append({
                                'artist': artist,
                                'song': song,
                                'lyrics': lyrics
                            })
        
        print(f" Encontradas {len(eminem_songs)} músicas do Eminem")
        
        if not eminem_songs:
            print(" Nenhuma música do Eminem encontrada no dataset")
            print(" O dataset pode ser mais focado em música anterior a 2010")
            return
        
        # Analisar as músicas do Eminem
        print(f"\n Analisando {len(eminem_songs)} músicas do Eminem...\n")
        
        for i, song_data in enumerate(eminem_songs, 1):
            artist = song_data['artist']
            song_name = song_data['song']
            lyrics = song_data['lyrics']
            
            print(f" {i:2d}. {song_name[:35]:35}", end=" ")
            
            sentiment = simulate_sentiment_analysis(lyrics)
            sentiment_counts[sentiment] += 1
            
            print(f"→ {sentiment}")
            
            # Pequena pausa para visualização
            time.sleep(0.5)
                
    except Exception as e:
        print(f" Erro: {e}")
        return
    
    # Salvar resultados
    with open('sentiment_eminem_results.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("      RESULTADOS - SENTIMENTOS DAS MÚSICAS DO EMINEM\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(" ARTISTA: Eminem\n")
        f.write(f" Total de músicas analisadas: {len(eminem_songs)}\n\n")
        
        f.write(" DISTRIBUIÇÃO DE SENTIMENTOS:\n")
        f.write("-" * 40 + "\n")
        
        total = sum(sentiment_counts.values())
        for sentiment in ["Positiva", "Neutra", "Negativa"]:
            count = sentiment_counts[sentiment]
            percentage = (count / total) * 100 if total > 0 else 0
            f.write(f" {sentiment}: {count:2d} músicas ({percentage:5.1f}%)\n")
        
        f.write(f"\n LISTA DE MÚSICAS ANALISADAS:\n")
        f.write("-" * 40 + "\n")
        for i, song_data in enumerate(eminem_songs, 1):
            sentiment = simulate_sentiment_analysis(song_data['lyrics'])
            f.write(f"{i:2d}. {song_data['song']} → {sentiment}\n")
        
        f.write(f"\n ANÁLISE:\n")
        f.write("   As músicas do Eminem frequentemente exploram temas complexos\n")
        f.write("   como struggles pessoais, crítica social e auto-reflexão.\n")
        f.write("   Esta análise por palavras-chave captura tendências gerais.\n")
        
        f.write(f"\n Data: {time.strftime('%d/%m/%Y %H:%M')}\n")
    
    # Mostrar resultados
    print("\n" + "" * 25)
    print("      ANÁLISE DO EMINEM CONCLUÍDA!")
    print("" * 25)
    
    print(f"\n RESULTADOS DAS {len(eminem_songs)} MÚSICAS:")
    print("-" * 45)
    total = sum(sentiment_counts.values())
    for sentiment in ["Positiva", "Neutra", "Negativa"]:
        count = sentiment_counts[sentiment]
        percentage = (count / total) * 100
        print(f" {sentiment}: {count:2d} músicas ({percentage:5.1f}%)")
    
    # Análise interpretativa
    print(f"\n INTERPRETAÇÃO:")
    if sentiment_counts['Negativa'] > sentiment_counts['Positiva']:
        print("   → Eminem tende a explorar temas mais intensos e dark")
    elif sentiment_counts['Positiva'] > sentiment_counts['Negativa']:
        print("   → Balanço mais positivo nas letras analisadas")
    else:
        print("   → Equilíbrio entre temas positivos e negativos")
    
    print(f"\n Resultados detalhados em: sentiment_eminem_results.txt")

if __name__ == "__main__":
    main()