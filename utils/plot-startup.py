import matplotlib.pyplot as plt
import seaborn as sns
import random
import pandas as pd

# Genera i dati mock
data = [{"tempo di esecuzione": round(random.gauss(23, 1), 3)} for _ in range(9)]
df = pd.DataFrame(data)

# Creazione del boxplot con grafico più largo e barra più stretta
plt.figure(figsize=(10, 6))  # Grafico più largo
ax = sns.boxplot(y=df["tempo di esecuzione"], width=0.3, flierprops={"marker": "o", "color": "red", "markersize": 8}, color="lightgreen")

# Calcolo della media
mean_value = df["tempo di esecuzione"].mean()

# Aggiungi il testo della media alla base
plt.text(0, 0, f'Media: {mean_value:.2f}', ha='center', va='bottom', fontsize=14, fontweight='bold', color="black")

# Imposta i label con font più grande
plt.ylabel("Downtime (s)", fontsize=14)
plt.xticks([])  # Rimuove i tick sull'asse X
plt.yticks(fontsize=12)

# Mostra griglia leggera
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Salva il plot
plt.tight_layout()
plt.savefig("benchmark/boxplot_failover.png")
plt.show()
