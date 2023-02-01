import pathlib
import pandas as pd

from pprint import pprint

inout_operations = ['Compra', 'Venda', 'Transferência - Liquidação']

products = {} # TODO make this a DataFrame with data info of the last operation
money_in = 0
money_out = 0

def parse_monetary_amount(string: str) -> float:
    try:
        parsed_string = string.split('R$')[1].replace('.','').replace(',', '.')
        return float(parsed_string)
    except:
        return 0

dir = pathlib.Path(__file__).resolve().parent.joinpath('movimentações')
files_in_basepath = dir.iterdir()
for item in files_in_basepath:
    df = pd.read_csv(item)
    rows, _ = df.shape

    for i in range(0, rows):
        product = df['Produto'][i]
        direction = df['Entrada/Saída'][i]
        amount = parse_monetary_amount(df['Valor da Operação'][i])
        operation = df['Movimentação'][i]
        if operation in inout_operations:
            if products.get(product) is None:
                products[product] = 0

            if  direction == 'Credito':
                money_in += float(amount)
                products[product] -= float(amount)
            else: # df['Entrada/Saída'][i] == 'Débito'
                money_out += float(amount)
                products[product] += float(amount)

print(f'Total: In R${money_in:.2f} | Out R${money_out:.2f}')
pprint(products)