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

from argparse import _ArgumentGroup
from dataclasses import dataclass
from functions import compound_interest as f, accumulate_index as acc
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


default_time_frame = 15 # years
default_budget = 15000
default_spences = 5000
default_house_value = 200000
default_rent = default_house_value*0.005 # 5% of house value
default_inflation = 6 # percentage
default_hpi = 8 # percentage
default_apy = 10 # percentage


def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('buy_vs_rent')
    interest_rate = parser.add_mutually_exclusive_group()
    interest_rate.add_argument('-iy', '--APY',
        type=float,
        help=f'annual percentage yield. Default is {default_apy}%%',
        metavar='',
        default=default_apy
    )
    interest_rate.add_argument('-im', '--MPY',
        type=float,
        help=f'optinal monthly interest rate. If set, it computes the actual APY',
        metavar='',
        default=0
    )
    parser.add_argument('-y', '--years',
        type=int,
        help=f'years to simulate. Default is {default_time_frame}',
        metavar='',
        default=default_time_frame
    )
    parser.add_argument('-b', '--budget',
        type=float,
        help=f'monthly budget. Default is {default_budget}',
        metavar='',
        default=default_budget
    )
    parser.add_argument('-r', '--rent',
        type=float,
        help=f'rent value. Default is 0.5%% of house value {default_rent}',
        metavar='',
        default=default_rent
    )
    parser.add_argument('-s', '--spences',
        type=float,
        help=f'avg monthly spences (rent not included). Default {default_spences}',
        metavar='',
        default=default_spences
    )
    parser.add_argument('-hv', '--house',
        type=float,
        help=f'house value. Default is {default_house_value}',
        metavar='',
        default=default_house_value
    )
    parser.add_argument('-if', '--inflation',
        type=float,
        help=f'inflation index (Brazil\'s IPCA). Default is {default_inflation}',
        metavar='',
        default=default_inflation
    )
    parser.add_argument('-hi', '--hpi',
        type=float,
        help=f'house price index (Brazil\'s IGPM). Default is {default_hpi}',
        metavar='',
        default=default_hpi
    )


def compute_indexes(kwargs: dict) -> dict:
    mpy = kwargs.get('MPY') / 100
    apy = kwargs.get('APY') / 100
    inflation = kwargs.get('inflation') / 100
    hpi = kwargs.get('hpi') / 100

    actual_apy = pow(1 + mpy, 12) - 1 if mpy else apy
    return {
        'apy': actual_apy,
        'inflation': inflation,
        'hpi': hpi
    }


def compute_values_corrected_by_index_over_time(
    initial_values: dict,
    indexes: dict,
    time_frame: np.array
) -> dict:
    budget = initial_values.get('budget')
    spences = initial_values.get('spences')
    rent = initial_values.get('rent')
    house_value = initial_values.get('house')
    inflation = indexes.get('inflation')
    hpi = indexes.get('hpi')
    return {
        'budget': budget*acc(time_frame, inflation, 'strict'),
        'spences': spences*acc(time_frame, inflation),
        'rent': rent*acc(time_frame, hpi, 'strict'),
        'house_value': house_value*acc(time_frame, hpi, 'strict')
    }


def get_time_frame(kwargs: dict) -> np.array:
    resolution = 4
    years = kwargs.get('years', default_time_frame)
    return np.linspace(0, years, (years*resolution)+1)


def get_plot_data_for_buy(
    apy: float,
    time_frame: np.array,
    values: dict,
    add_house_value: bool = False
) -> PlotData:
    investment_budget = values['budget']-values['spences']
    accumulated_value = f(time_frame, apy, 0, investment_budget)
    return PlotData(
        x = time_frame,
        y = accumulated_value + (0 if not add_house_value else values['house_value']),
        additional_data = [
            Stats(
                budget=values['budget'][i],
                spences=values['spences'][i],
                rent=0,
                interest=accumulated_value[i]*(pow(1+apy, 1/12)-1),
                house_value=values['house_value'][i]
            )
        for i, _ in enumerate(time_frame)]
    )


def get_plot_data_for_rent(
    apy: float,
    time_frame: np.array,
    values: dict
) -> PlotData:
    initial_deposit = values['house_value'][0]
    investment_budget = values['budget']-values['spences']-values['rent']
    accumulated_value = f(time_frame, apy, initial_deposit, investment_budget)
    return PlotData(
        x = time_frame,
        y = accumulated_value,
        additional_data = [
            Stats(
                budget=values['budget'][i],
                spences=values['spences'][i],
                rent=values['rent'][i],
                interest=accumulated_value[i]*(pow(1+apy, 1/12)-1),
                house_value=0
            )
        for i, _ in enumerate(time_frame)]
    )


def get_plot_title(indexes, values):
    apy = indexes['apy']
    inflation = indexes['hpi']
    hpi = indexes['hpi']
    budget = values['budget'][0]
    house_value = values['house_value'][0]
    rent = values['rent'][0]
    spences = values['spences'][0]
    return f'APY {apy*100:.1f}% | IPCA {inflation*100:.2f}% | IGPM {hpi*100:.2f}% \n Budget R\\$ {budget:.0f} | Imóvel R\\$ {house_value:.0f} | Aluguel R\\$ {rent:.0f} | Despesas R\\$ {spences:.0f}'


def run(*args,**kwargs):
    time_frame = get_time_frame(kwargs)
    indexes = compute_indexes(kwargs)
    values = compute_values_corrected_by_index_over_time(kwargs, indexes, time_frame)

    scale = 1.1
    fig, ax = plt.subplots(figsize=(16*scale,9*scale))

    data0 = get_plot_data_for_rent(indexes['apy'], time_frame, values)
    ax.plot(data0.x, data0.y, color='b', label=f'total investido - aluguel')
    cursor0 = SnappingCursor(ax, data0, {'color': 'b'})
    fig.canvas.mpl_connect('motion_notify_event', cursor0.on_mouse_move)

    data1 = get_plot_data_for_buy(indexes['apy'], time_frame, values)
    ax.plot(data1.x, data1.y, color='r', label=f'total investido - casa própria')
    cursor1 = SnappingCursor(ax, data1, {'color': 'r', 'x': 0.95})
    fig.canvas.mpl_connect('motion_notify_event', cursor1.on_mouse_move)

    data2 = get_plot_data_for_buy(indexes['apy'], time_frame, values, True)
    ax.plot(data2.x, data2.y, color='g', label=f'patrimônio total com imóvel')

    ax.grid(linestyle='-', linewidth=1)
    ax.set_xlabel("Anos")
    ax.set_ylabel("Patrimônio")
    plt.axis(xmin=0, xmax=time_frame[-1], ymin=0)
    plt.title(get_plot_title(indexes, values))
    plt.legend()
    plt.show()
