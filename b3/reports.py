import pandas as pd

from dataclasses import dataclass

from repositories.transactions import (
    Transactions, CREDIT, DEBIT, TRADES_OPS, DIVIDENDS_OPS,
    get_transaction_from_csv as get_transactions,
)
from repositories.position import Position, get_position_from_csv as get_position
from repositories.utils import to_moneraty_string


@dataclass
class ProductReport:
    name: str
    current: int = 0
    bought: int = 0
    sold: int = 0
    dividends: int = 0
    transactions: Transactions = None

    def print_summary(self, full=False):
        title = f'{self.name: ^20}'
        print(f'{title:-^50}')

        if full:
            print(self.transactions)
            print('-'*50)

        print(f'Compra: {to_moneraty_string(self.bought)}')
        print(f'Venda: {to_moneraty_string(self.sold)}')
        print(f'Lucro: {to_moneraty_string(self.get_gains())}')
        print(f'Divindendos: {to_moneraty_string(self.dividends)}')
        print('\n')

    def get_gains(self):
        """ realized profit """
        if self.sold == 0:
            return 0

        return self.current - (self.bought - self.sold)


@dataclass
class FullReport(ProductReport):
    name: str = 'B3 Report'
    gains: int = 0

    def add(self, report: ProductReport):
        self.current += report.current
        self.bought += report.bought
        self.sold += report.sold
        self.dividends += report.dividends
        self.gains += report.get_gains()
        if self.transactions is None or self.transactions.empty:
            self.transactions = report.transactions
        else:
            self.transactions = pd.concat([self.transactions, report.transactions], ignore_index=True)

    def get_gains(self):
        """must override parent"""
        return self.gains


def get_product_report(product: str, transactions: Transactions, position: Position) -> ProductReport:

    product_transactions = transactions.query(f'PRODUCT == "{product}" and QTY > 0 and VALUE > 0').reset_index()

    if(product_transactions.empty):
        return

    trades = product_transactions.query(f'OPERATION in {TRADES_OPS}').groupby('OPERATION_TYPE')['VALUE'].sum()
    dividends = product_transactions.query(f'OPERATION in {DIVIDENDS_OPS}').groupby('OPERATION_TYPE')['VALUE'].sum()
    product_position = position.query(f'PRODUCT == "{product}"')

    current_value = product_position.VALUE.iloc[0] if not product_position.empty else 0

    return ProductReport(
        product,
        current_value,
        trades.get(CREDIT, 0),
        trades.get(DEBIT, 0),
        dividends.get(CREDIT, 0),
        product_transactions
    )


def run():
    transactions_df = get_transactions().sort_values(by='PRODUCT')
    position_df = get_position().sort_values(by='PRODUCT')
    full_report = FullReport()

    for product in transactions_df.PRODUCT.unique():
        report = get_product_report(product, transactions_df, position_df)
        if report:
            report.print_summary(full=False)
            full_report.add(report)

    full_report.print_summary()


if __name__ == '__main__':
    run()
