""" Acumulado 2022 -> 5,79% """

montlhy_value = [0.54, 1.01, 1.62, 1.06, 0.47, 0.67, -0.68, -0.36, -0.29, 0.59, 0.41, 0.62]

def gmean(series):
    acc = 1
    for value in series:
        acc *= 1 + value/100
    return (pow(acc, 1/(len(series))) - 1)*100


monthly_mean = sum(montlhy_value)/len(montlhy_value)
monthly_gmean = gmean(montlhy_value)

anual_sum = sum(montlhy_value)
anual_mean = (pow(1 + monthly_mean/100, 12) - 1) * 100
anual_gmean = (pow(1 + monthly_gmean/100, 12) - 1) * 100

print(f'Soma simple: {anual_sum}')
print(f'Média simples acumulada: {anual_mean}')
print(f'Média geométrica acumulada: {anual_gmean}')