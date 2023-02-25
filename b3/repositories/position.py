import pathlib
import pandas as pd

from pandera import SchemaModel
from pandera.typing import Series

from .utils import parse_product_code, parse_monetary_amount, parse_numerical_string


class Position(SchemaModel):
    PRODUCT: Series[str]
    VALUE: Series[int]
    QTY: Series[float]


def get_position_from_csv() -> Position:
    path = pathlib.Path(__file__).resolve().parents[1].joinpath('data/position')
    files_in_basepath = path.iterdir()

    dfs = [pd.read_csv(item, dtype={'Quantidade': str}) for item in files_in_basepath]
    df = pd.concat(dfs, ignore_index=True)

    df['Produto'] = df['Produto'].apply(parse_product_code)
    df['Valor_Atualizado'] = df['Valor Atualizado'].apply(parse_monetary_amount)

    return Position(pd.DataFrame({
        'PRODUCT': df['Produto'].apply(parse_product_code),
        'VALUE': df['Valor Atualizado'].apply(parse_monetary_amount),
        'QTY': df['Quantidade'].apply(parse_numerical_string)
    }))

