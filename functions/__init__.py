import numpy as np

def compound_interest(
    years: float,
    APY: float,
    initial_deposit: float,
    recuring_deposit: float = 0, n=12
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


def correct_by_index(x, index, type = 'continuous'):
    # TODO improve this argument name and strategy
    correction_type = {
        'continuous': lambda x, index: pow(1 + index, x),
        'strict': lambda x, index: pow(1 + index, np.floor(x))
    }
    return correction_type[type](x, index)
