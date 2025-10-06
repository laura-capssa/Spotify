#!/bin/bash

echo "=== Spotify Data Analysis ==="

# Compilar código MPI
echo "1. Compilando código MPI..."
make clean
make

# Executar análise MPI
echo "2. Executando análise MPI..."
mpirun -np 4 ./spotify_mpi spotify_millsongdata.csv

# Combinar resultados
echo "3. Combinando resultados parciais..."
python3 python/reducer.py

# Classificação de sentimentos (opcional - requer Ollama)
echo "4. Executando classificação de sentimentos..."
cd python
if command -v ollama &> /dev/null && ollama list &> /dev/null; then
    python3 classify_ollama.py ../spotify_millsongdata.csv
else
    echo "Ollama não encontrado ou não está rodando. Pulando classificação de sentimentos."
    echo "Instale e inicie o Ollama: https://ollama.com"
    echo "Execute: ollama pull llama2"
fi
cd ..

echo "=== Análise Concluída ==="
echo "Resultados:"
echo "- Contagem de palavras: total_word_counts.txt"
echo "- Artistas mais frequentes: total_artist_counts.txt"
if [ -f "python/sentiment_results.txt" ]; then
    echo "- Sentimentos: python/sentiment_results.txt"
fi