import numpy as np
import matplotlib.pyplot as plt

from functions import compound_interest as f

initial_deposit = 10000
time_frame = 30 # years
mothly_interest_rates = [0.002, 0.004, 0.006, 0.008, 0.01, 0.012]
APY = [ pow(1+i, 12) - 1 for i in mothly_interest_rates]

years = np.linspace(0, time_frame, time_frame+1)

def run():
    for i in APY:
        plt.plot(years, f(years, i, initial_deposit, n=1), label=f'{i*100:.1f}% ao ano')
    plt.grid(linestyle='-', linewidth=1)
    plt.axis(xmin=0, xmax=time_frame, ymin=0)
    plt.xlabel("Anos")
    plt.ylabel("Quantia")
    plt.legend()
    plt.title('Juros composto')
    plt.show()
