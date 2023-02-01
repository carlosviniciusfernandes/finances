
import argparse

import projections

plot_choices = ['buy_vs_rent', 'compound_interest', 'compound_interest_with_recurring_deposit']

parser = argparse.ArgumentParser(
    prog = 'Run Projection',
    description = 'Runs a given financial simulation',
    epilog = 'Generetes a Matplotlib plot',
)
parser.add_argument('--plot',
    choices=plot_choices,
    metavar=f'\t\t' + '; '.join(plot_choices),
    required=True
)

if __name__ == "__main__":
    args = parser.parse_args()
    getattr(projections, f'plot_{args.plot}').run()