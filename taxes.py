def calculate_IRRF(monthly_income, number_dependants = 0):
    tax_brackets = {
        'tier_1': { 'min': 0, 'max': 1903.98, 'rate': 0, 'discount': 0 },
        'tier_2': { 'min': 1903.98, 'max': 2826.25, 'rate': 7.5,'discount': 142.80 },
        'tier_3': { 'min': 2826.25, 'max': 3751.06, 'rate': 15,'discount': 354.80 },
        'tier_4': { 'min': 3751.06, 'max': 4664.68, 'rate': 22.5, 'discount': 636.13 },
        'tier_5': { 'min': 4664.68, 'max': float('inf'), 'rate': 27.5,'discount': 636.13 },
    }
    dependant_discount = 189.59

    for _, values in tax_brackets.items():
        if(values['min'] < monthly_income and monthly_income <= values['max']):
            return monthly_income*values['rate']/100 - values['discount'] - number_dependants*dependant_discount


def calculate_INSS(monthly_income):
    tax_brackets = [
        { 'min': 0, 'max': 1302, 'rate': 7.5 },
        { 'min': 1302, 'max': 2571.29, 'rate': 9 },
        { 'min': 2571.29, 'max': 3856.94, 'rate': 12 },
        { 'min': 3856.94, 'max': 7507.49, 'rate': 14 }
    ]

    taxed_value = 0
    for tax_tier in tax_brackets:
        tier_diff = min(monthly_income - tax_tier['min'], tax_tier['max'] - tax_tier['min'])
        if(tier_diff > 0):
            taxed_value += tier_diff*tax_tier['rate']/100
    return taxed_value


def calculate_CLT(raw_monthly_salary):
    inss = calculate_INSS(raw_monthly_salary)
    irrf = calculate_IRRF(raw_monthly_salary - inss)
    after_taxes = raw_monthly_salary - inss - irrf
    print(f'INSS: RS {inss:.2f}\nIRRF: RS {irrf:.2f}\nLíquido: RS {after_taxes:.2f}')
    return after_taxes


def calculate_DAS(revenue):
    pass