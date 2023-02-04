import pathlib

import projections.plot_compound_interest as compound_interest
import projections.plot_compound_interest_with_recurring_deposits as compound_interest_with_recurring_deposits
import projections.plot_buy_vs_rent as buy_vs_rent

dir = pathlib.Path(__file__).resolve().parent
files_in_basepath = dir.iterdir()
plot_choices = [item.name.removeprefix('plot_').removesuffix('.py') for item in files_in_basepath if 'plot_' in item.name]
