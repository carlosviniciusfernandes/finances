import numpy as np
import matplotlib.pyplot as plt
from plot_utils.cursor import SnappingCursor

"""
Valores acumulados (12 meses) dos índices de 1995 a 2022

Dados mensais
            igpm      ipca
média       0.092341  0.069018
mediana     0.080700  0.061500
desvio      0.069668  0.039947
geométrica  0.090238  0.068308

Dados Anuais
            igpm      ipca
média       0.090554  0.069021
mediana     0.077850  0.059100
desvio      0.064209  0.038639
geométrica  0.088714  0.068358

"""

budget = 15000
spences = 6000
house_value = 200000
# rent = house_value*0.009
rent = 1500

inflation = 0.06
hpi = 0.08

mothly_interest_rates = [0.002, 0.004, 0.006, 0.008, 0.01, 0.012, 0.014, 0.016]
APY = [ pow(1+i, 12) - 1 for i in mothly_interest_rates]
i = 3

time_frame = 15 # years
years = np.linspace(0, time_frame, (time_frame*4)+1)

def correct_by_index(x, index):
    return  pow(1 + index, np.floor(x)) # corrected anually, not monthly

def f(x, i, initial_deposit, recuring_deposit, index=inflation):
    n = 12 # number of time rate is applied
    corrected_recuring_deposit = recuring_deposit*correct_by_index(x, index)
    return initial_deposit*pow((1+(i/n)), n*x) +  corrected_recuring_deposit*(pow(1+(i/n), n*x)-1)/(i/n)

fig, ax = plt.subplots(figsize=(16,9))

line1, = ax.plot(years, f(years, APY[i], 0, budget-spences), color='r', label=f'total investido - casa própria')
cursor1 = SnappingCursor(ax, line1, {'text_color': 'r'})
fig.canvas.mpl_connect('motion_notify_event', cursor1.on_mouse_move)

line2, = ax.plot(years, f(years, APY[i], house_value, budget-spences-rent), color='b', label=f'total investido - aluguel')
cursor2 = SnappingCursor(ax, line2, {'text_color': 'b', 'ypos':-0.02})
fig.canvas.mpl_connect('motion_notify_event', cursor2.on_mouse_move)

line3, = ax.plot(years, f(years, APY[i], 0, budget-spences) + house_value*correct_by_index(years, hpi), color='g', label=f'patrimônio total com imóvel')
cursor3 = SnappingCursor(ax, line3, {'text_color': 'g', 'ypos':-0.04})
fig.canvas.mpl_connect('motion_notify_event', cursor3.on_mouse_move)

line4, = ax.plot(years, spences*correct_by_index(years, 2*inflation), color='m', label=f'despesa mensal')
cursor4 = SnappingCursor(ax, line4, {'text_color': 'm', 'ypos':-0.06})
fig.canvas.mpl_connect('motion_notify_event', cursor4.on_mouse_move)

ax.grid(linestyle='-', linewidth=1)
ax.set_xlabel("Anos")
ax.set_ylabel("Patrimônio")
plt.axis(xmin=0, xmax=time_frame, ymin=0)
plt.title(f'APY {APY[i]*100:.1f}% | IPCA {inflation*100:.2f}% | IGPM {hpi*100:.2f}% \n Budget R\\$ {budget} | Imóvel R\\$ {house_value} | Aluguel R\\$ {rent} | Despesas R\\$ {spences}')
plt.legend()
plt.show()
