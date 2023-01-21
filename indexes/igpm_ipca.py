import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# os valor dos índices já é o acumulado calculado para aquele mês
df = pd.read_csv('igpm_ipca_1995-2022_anual.csv')

normalized_df = pd.DataFrame()
normalized_df['ipgm'] = df['IGPM']/100
normalized_df['ipca'] = df['IPCA']/100

def gmean(series: pd.Series):
    acc = 1
    for value in series:
        acc *= 1 + value
    return pow(acc, 1/(len(series))) - 1

def compute_stats(series: pd.Series):
    return {
        'mean': np.mean(series),
        'median': np.median(series),
        'std': np.std(series),
        'gmean': gmean(series),
    }

stats_df = pd.DataFrame()
stats_df['igpm'] = compute_stats(normalized_df['ipgm'])
stats_df['ipca'] = compute_stats(normalized_df['ipca'])
print(stats_df)

normalized_df.plot()
plt.show()