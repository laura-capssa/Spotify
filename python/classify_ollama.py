
"""
Classifica cada letra em Positiva / Neutra / Negativa usando Ollama (CLI).

Requisitos:
- Ollama instalado e modelo local disponível (ex: llama2, mistral, etc.)
- CSV no formato: track_id,artist_name,lyrics

Uso:
    python3 python/classify_ollama.py example_dataset.csv --model llama2

Saídas:
- classification_counts.csv (classe,contagem)
- classification_by_track.csv (track_id,classe)
"""
import csv
import argparse
import subprocess
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('csvfile')
parser.add_argument('--model', required=True, help='nome do modelo local em Ollama (ex: llama2)')
parser.add_argument('--prompt', default=None, help='prompt opcional')
args = parser.parse_args()

MODEL = args.model
PROMPT = args.prompt or (
    "Classifique a seguinte letra em uma das três classes: Positiva, Neutra, Negativa. "
    "Responda apenas com uma palavra: Positiva, Neutra ou Negativa.\nLetra:\n\n"
)

counts = Counter()
with open(args.csvfile, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
       
        track_id = row[0]
        lyrics = row[2] if len(row) > 2 else ''
        if not lyrics.strip():
            cls = 'Neutra'
        else:
            prompt = PROMPT + lyrics.replace('"', '\\"')
            try:
                res = subprocess.run(
                    ['ollama', 'run', MODEL, '--prompt', prompt],
                    capture_output=True, text=True, timeout=30
                )
                out = res.stdout.strip().splitlines()[-1].strip()
                if 'posit' in out.lower():
                    cls = 'Positiva'
                elif 'negat' in out.lower():
                    cls = 'Negativa'
                else:
                    cls = 'Neutra'
            except Exception as e:
                print('Erro ao chamar ollama:', e)
                cls = 'Neutra'
        counts[cls] += 1
        with open('classification_by_track.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([track_id, cls])

with open('classification_counts.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['class', 'count'])
    for k, v in counts.items():
        writer.writerow([k, v])

print('✅ Classificação concluída. Arquivos: classification_counts.csv e classification_by_track.csv')
