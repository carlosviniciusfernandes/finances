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
import numpy as np
import matplotlib.pyplot as plt

from dataclasses import dataclass
from functions import compound_interest as f, correct_by_index
from plot_utils.cursor import SnappingCursor
from plot_utils.plot_data import PlotData

@dataclass
class Stats:
    budget: float
    spences: float
    rent: float
    house_value: float
    interest: float

    def __repr__(self) -> str:
        return \
            f'budget:{self.budget:.0f}' + \
            f'\nspences:{self.spences:.0f}' + \
            f'\nrent: {self.rent:.0f}' + \
            f'\ntotal spent: {self.spences + self.rent:.0f}' + \
            f'\ninterest: {self.interest:.0f}' + \
            f'\nhouse: {self.house_value:.0f}'

budget = 20000
spences = 6000
house_value = 220000
# rent = house_value*0.009
rent = 1600

inflation = 0.06
hpi = 0.08

mothly_interest_rates = [0.002, 0.004, 0.006, 0.008, 0.01, 0.012, 0.014, 0.016]
APY = [ pow(1+i, 12) - 1 for i in mothly_interest_rates]
r = 3

time_frame = 15 # years
years = np.linspace(0, time_frame, (time_frame*4)+1)

#TODO better naming this hash
df = {
    'budget': budget*correct_by_index(years, inflation, 'strict'),
    'spences': spences*correct_by_index(years, inflation),
    'rent': rent*correct_by_index(years, hpi, 'strict'),
    'house_value': house_value*correct_by_index(years, hpi, 'strict')
}

investment_budget = df['budget']-df['spences']-df['rent']
data0 = PlotData(
    x = years,
    y = f(years, APY[r], house_value, investment_budget),
    additional_data = [
        Stats(
            budget=df['budget'][i],
            spences=df['spences'][i],
            rent=df['rent'][i],
            interest=f(year, APY[r], house_value, investment_budget[i])*mothly_interest_rates[r],
            house_value=0
        )
    for i, year in enumerate(years)]
)

investment_budget=df['budget']-df['spences']
data1 = PlotData(
    x = years,
    y = f(years, APY[r], 0, investment_budget),
    additional_data = [
        Stats(
            budget=df['budget'][i],
            spences=df['spences'][i],
            house_value=df['house_value'][i],
            interest=f(year, APY[r], 0, investment_budget[i])*mothly_interest_rates[r],
            rent=0
        ) for i, year in enumerate(years)
    ]
)

data2 = PlotData(
    x = years,
    y = data1.y + df['house_value'],
)

def run():
    fig, ax = plt.subplots(figsize=(16,9))

    ax.plot(data0.x, data0.y, color='b', label=f'total investido - aluguel')
    cursor0 = SnappingCursor(ax, data0, {'color': 'b'})
    fig.canvas.mpl_connect('motion_notify_event', cursor0.on_mouse_move)

    ax.plot(data1.x, data1.y, color='r', label=f'total investido - casa própria')
    cursor1 = SnappingCursor(ax, data1, {'color': 'r', 'x': 0.95})
    fig.canvas.mpl_connect('motion_notify_event', cursor1.on_mouse_move)

    ax.plot(data2.x, data2.y, color='g', label=f'patrimônio total com imóvel')

    ax.grid(linestyle='-', linewidth=1)
    ax.set_xlabel("Anos")
    ax.set_ylabel("Patrimônio")
    plt.axis(xmin=0, xmax=time_frame, ymin=0)
    plt.title(f'APY {APY[r]*100:.1f}% | IPCA {inflation*100:.2f}% | IGPM {hpi*100:.2f}% \n Budget R\\$ {budget} | Imóvel R\\$ {house_value} | Aluguel R\\$ {rent} | Despesas R\\$ {spences}')
    plt.legend()
    plt.show()
