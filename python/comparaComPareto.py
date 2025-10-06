import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Ler o CSV
df = pd.read_csv("frequencias.csv")  # substitua pelo nome do seu arquivo

# 2️⃣ Ordenar pela frequência decrescente
df = df.sort_values(by="count", ascending=False)

# 3️⃣ Calcular percentual individual e acumulado
total = df['count'].sum()
df['percent'] = df['count'] / total * 100
df['cumulative_percent'] = df['percent'].cumsum()

# 4️⃣ Identificar quantas palavras representam ~80% do total
pareto_count = df[df['cumulative_percent'] <= 80].shape[0]
print(f"As {pareto_count} palavras mais frequentes representam aproximadamente 80% das ocorrências.")

# 5️⃣ Plotar gráfico de Pareto
fig, ax1 = plt.subplots(figsize=(12,6))

# Barras de frequência
ax1.bar(df['word'], df['count'], color='skyblue')
ax1.set_xlabel('Palavras')
ax1.set_ylabel('Frequência')
ax1.tick_params(axis='x', rotation=90)

# Linha de percentual acumulado
ax2 = ax1.twinx()
ax2.plot(df['word'], df['cumulative_percent'], color='red', marker='o', linewidth=2)
ax2.set_ylabel('Percentual acumulado (%)')

# Linha horizontal de 80% para referência
ax2.axhline(y=80, color='green', linestyle='--', linewidth=1.5)
plt.title('Distribuição de Frequência de Palavras vs Pareto')

plt.tight_layout()
plt.show()