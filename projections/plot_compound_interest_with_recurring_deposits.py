import numpy as np
import matplotlib.pyplot as plt

from argparse import _ArgumentGroup
from functions import compound_interest as f
from plot_utils.cursor import Cursor

default_time_frame = 15 # years
default_initial_deposit = 100000
default_recurring_deposit = 5000 # montlhy
mothly_interest_rates = [0.002, 0.004, 0.006, 0.008, 0.01, 0.012]
APY = [ pow(1+i, 12) - 1 for i in mothly_interest_rates]

def add_command(subparsers: _ArgumentGroup):
    parser = subparsers.add_parser('compound_interest_with_recurring_deposits')
    parser.add_argument('-y', '--years',
        type=int,
        help=f'years to simulate. Default is {default_time_frame}',
        metavar='',
        default=default_time_frame
    )
    parser.add_argument('-i', '--initial',
        type=float,
        help=f'initial amount to which interest is applied over time. Default is {default_initial_deposit}',
        metavar='',
        default=default_initial_deposit
    )
    parser.add_argument('-d', '--deposits',
        type=float,
        help=f'recurring deposits that interest is applied over time. Default is {default_recurring_deposit}',
        metavar='',
        default=default_recurring_deposit
    )

def run(*args, **kwargs):
    years = kwargs.get('years', default_time_frame)
    initial_deposit = kwargs.get('initial', default_initial_deposit)
    recurring_deposit = kwargs.get('deposits', default_recurring_deposit)

    resolution = 4
    time_frame = np.linspace(0, years, (years*resolution)+1)

    fig, ax = plt.subplots()
    for i in APY:
        ax.plot(time_frame, f(time_frame, i, initial_deposit, recurring_deposit), label=f'{i*100:.1f}% APY')
    cursor = Cursor(ax)
    fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)

    plt.grid(linestyle='-', linewidth=1)
    plt.xlabel("Years")
    plt.ylabel("Accumulated Amount")
    plt.axis(xmin=0, xmax=years, ymin=initial_deposit)
    plt.legend()
    plt.title('Compound Interest with Recurring Deposits')
    plt.show()
