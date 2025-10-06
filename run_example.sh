

echo "🚀 Compilando o código MPI..."
make

echo "🧠 Executando o processamento em paralelo..."
mpirun -n 4 ./spotify_mpi example_dataset.csv

echo "📊 Agregando resultados com Python..."
python3 python/reducer.py

echo "🎵 Classificando letras com Ollama (exemplo com modelo llama2)..."


echo "✅ Processo completo!"
echo "Arquivos finais esperados:"
echo " - final_word_counts.csv"
echo " - top_artists.csv"
echo " - classification_counts.csv (se classificação for executada)"
