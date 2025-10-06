
import sys
import glob
from collections import defaultdict





def merge_partials(pattern):
counts = defaultdict(int)
for fname in glob.glob(pattern):
with open(fname, 'r', encoding='utf-8') as f:
for line in f:
parts = line.rstrip('\n').split('\t')
if len(parts) != 2: continue
k, v = parts[0], int(parts[1])
counts[k] += v
return counts


if __name__ == '__main__':
words = merge_partials('partial_words_*.txt')
artists = merge_partials('partial_artists_*.txt')


# salvar final_word_counts.csv (palavra,contagem)
with open('final_word_counts.csv','w',encoding='utf-8') as f:
f.write('word,count\n')
for w,c in sorted(words.items(), key=lambda x: -x[1]):
f.write(f'{w},{c}\n')


with open('top_artists.csv','w',encoding='utf-8') as f:
f.write('artist,count\n')
for a,c in sorted(artists.items(), key=lambda x: -x[1]):
f.write(f'{a},{c}\n')


print('Arquivos gerados