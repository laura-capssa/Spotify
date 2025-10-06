# Spotify
Processamento paralelo com C e MPI

Desenvolver uma aplicação em paralelo utilizando o MPI com C para processar em paralelo os dados referentes a músicas no Spotify (https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset), o trabalho consistirá em obter três tipos de informação do dataset, sendo elas:

1 - Contagem de palavras: Contar a aparição de cada palavra presente nas letras, este desafio irá compor 40% da nota do código.
2 - Artistas com mais músicas: Encontrar os artistas com a maior quantidade de músicas, este desafio irá compor 40% da nota do código.
3 - Classificação: Fazer a classificação entre "Positiva", "Neutra" e "Negativa" sobre a letra das músicas usando uma integração com um modelo local de linguagem, após a classificação deve ser contado o total de cada classe, para este desafio pode ser utilizado uma linguagem auxiliar, como o python, para fazer a chamada do LLM, além de um software para auxiliar na execução do modelo, como por exemplo o Ollama (https://ollama.com). Este desafio irá compor 20% da nota do código.

- Para a entrega anexar todos os arquivos necessários para executar a solução.
- Calcular as métricas de desempenho da aplicação, analisando o que impactou o resultado.





# Relatório - Processamento Paralelo de Dataset do Spotify

## Resultados Obtidos

### 1. Contagem de Palavras (40%)
- **Total de palavras únicas**: 1,558
- **Palavras mais frequentes**:
  1. the (17,114)
  2. i (15,938) 
  3. you (13,012)
  4. a (10,670)
  5. to (7,718)

### 2. Artistas com Mais Músicas (40%)
- **Total de artistas únicos**: 2,259
- **Top 5 artistas**:
  1. Donna Summer (191 músicas)
  2. America (189 músicas)
  3. Gordon Lightfoot (189 músicas)
  4. Alabama (188 músicas)
  5. Bob Dylan (188 músicas)

### 3. Classificação de Sentimentos (20%)
- Integração com Ollama/Llama2 para análise
- Classificação em Positiva/Neutra/Negativa

## Métricas de Desempenho

### Speedup Observado:
- 1 processo: 45.2s
- 2 processos: 28.7s (1.57x speedup)
- 4 processos: 18.3s (2.47x speedup)

### Fatores que Impactaram o Desempenho:
- Overhead de comunicação MPI
- Balanceamento de carga entre processos
- Operações de I/O para arquivos intermediários
- Eficiência no parsing do formato CSV

## Tecnologias Utilizadas
- **MPI** para processamento paralelo
- **C** para contagem eficiente
- **Python** para redução e classificação
- **Ollama** para análise de sentimentos com LLM