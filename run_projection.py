
import argparse

import projections
def load_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'Run Projection',
        description = 'Runs a given financial simulation',
        epilog = 'Generetes a Matplotlib plot',
    )
    parser.add_argument('-l', '--list', help='list available plotting simulations', action='store_true')
    subparsers = parser.add_subparsers(help='name simulation to run', metavar='name', dest='plot_name')
    for plot in projections.plot_choices:
        getattr(projections, f'{plot}').add_command(subparsers)
    return parser

if __name__ == "__main__":
    parser = load_argument_parser()
    args = parser.parse_args()

    if(args.list):
        message = "Available scripts:"
        message += ''.join([f'\n  -{plot}' for plot in projections.plot_choices])
        print(message)
        exit()
    getattr(projections, f'{args.plot_name}').run(**vars(args))
