import numpy as np
import matplotlib.pyplot as plt

from argparse import _ArgumentGroup
from functions import compound_interest as f

default_initial_deposit = 10000
default_time_frame = 30 # years
mothly_interest_rates = [0.002, 0.004, 0.006, 0.008, 0.01, 0.012]
APY = [ pow(1+i, 12) - 1 for i in mothly_interest_rates]

def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('compound_interest')
    parser.add_argument('-y', '--years',
        type=int,
        help=f'years to simulate. Default is {default_time_frame}',
        metavar='',
        default=default_time_frame
    )
    parser.add_argument('-a', '--amount',
        type=float,
        help=f'amount to which interest is applied over time. Default is {default_initial_deposit}',
        metavar='',
        default=default_initial_deposit
    )

def run(*args, **kwargs):
    years = kwargs.get('years', default_time_frame)
    initial_deposit = kwargs.get('amount', default_initial_deposit)
    resolution = 4

    time_frame = np.linspace(0, years, (years*resolution)+1)
    for i in APY:
        plt.plot(time_frame, f(time_frame, i, initial_deposit, n=1), label=f'{i*100:.1f}% APY')
    plt.grid(linestyle='-', linewidth=1)
    plt.axis(xmin=0, xmax=years, ymin=initial_deposit)
    plt.xlabel("Years")
    plt.ylabel("Amount")
    plt.legend()
    plt.title('Compound Interest')
    plt.show()
