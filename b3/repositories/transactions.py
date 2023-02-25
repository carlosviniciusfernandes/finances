from dataclasses import dataclass

import pathlib
import pandas as pd

from datetime import datetime
from pandera import SchemaModel
from pandera.typing import Series

from .utils import parse_product_code, parse_monetary_amount, parse_numerical_string


CREDIT = 'Credito'
DEBIT = 'Debito'
TRADES_OPS = [
    'Compra',
    'Venda',
    'Transferência',
    'Transferência - Liquidação'
]
DIVIDENDS_OPS = [
    'Juros Sobre Capital Próprio',
    'Dividendo',
    'Rendimento',
]


class Transactions(SchemaModel):
    PRODUCT: Series[str]
    QTY: Series[float]
    DATE: Series[datetime]
    OPERATION: Series[str]
    OPERATION_TYPE: Series[str]
    VALUE: Series[int]


def get_transaction_from_csv() -> Transactions:
    path = pathlib.Path(__file__).resolve().parents[1].joinpath('data/transactions')
    files_in_basepath = path.iterdir()

    dfs = [pd.read_csv(item, dtype={'Quantidade': str}) for item in files_in_basepath]
    df = pd.concat(dfs, ignore_index=True)

    return Transactions(pd.DataFrame({
        'PRODUCT': df['Produto'].apply(parse_product_code),
        'QTY': df['Quantidade'].apply(parse_numerical_string),
        'DATE': pd.to_datetime(df['Data'], format='%d/%m/%Y'),
        'OPERATION': df['Movimentação'],
        'OPERATION_TYPE': df['Entrada/Saída'],
        'VALUE': df['Valor da Operação'].apply(parse_monetary_amount)
    }))
