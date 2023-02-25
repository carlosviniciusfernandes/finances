import numpy as np

def compound_interest(
    years: float,
    APY: float,
    initial_deposit: float,
    recuring_deposit: float = 0,
    n: int = 12
) -> float:
    """
    Args:
        years (float): Amount of time in years that interest is been applied to a deposit
        APY (float): Annual Percentage Yield
        initial_deposit (float): Initial monetary amount
        recuring_deposit (float): Montlhy recurring deposits. Defailt is 0 (no deposits made)
        n (int): Number of time rate is applied. Defatul is 12 (applies each month)
    Returns:
        accumulated (float): Acumulated value over time
    """
    return initial_deposit*pow((1+(APY/n)), n*years) +  recuring_deposit*(pow(1+(APY/n), n*years)-1)/(APY/n)


def accumulate_index(time_frame, index, type = 'continuous'):
    """
    Args:
        time_frame (float): time windows in wich the index is been accumulated (eg. 2.5 years)
        index (float): index itself
        type (string): ['continuous', 'strict']; execution type.
            - 'strict' round down the time frame to integer values,
                used to correct values that discrete steps (eg. salary is raised once for year).
            - 'continuous': default execution, used to correct values that are
                continuously changing (eg. inflation accumulates every month)
    Returns:
        accumulate_index (float): total accumulated index in the time window
    """
    run_strategy = {
        'continuous': lambda x, i: pow(1 + i, x),
        'strict': lambda x, i: pow(1 + i, np.floor(x))
    }
    return run_strategy[type](time_frame, index)
