def parse_monetary_amount(string: str) -> int:
    try:
        parsed_string = string.split('R$')[1].replace('.','').replace(',', '.')
        fractional_amount = float(parsed_string)
        return int(fractional_amount*100)
    except:
        return 0

def to_moneraty_string(value: int) -> str:
    return f'R${value/100:.2f}'

def parse_numerical_string(string: str) -> float:
    return float(string.replace('.','').replace(',', '.'))

def parse_product_code(string: str) -> str:
    return string.split('-')[0].strip()
