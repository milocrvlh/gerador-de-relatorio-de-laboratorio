import numpy as np
import pandas as pd
from tabulate import tabulate

# Dados de Volume do laboratório
volume = np.array([17., 16., 15., 14.5, 13.5, 12.5, 11.5, 10.5, 10.0, 9.5])

# Dados do Erro do Volume do laboratório
erro_volume = np.zeros(10)
erro_volume[2:] = 0.5

# Cálculo do Inverso do Volume
inverso_do_volume = 1 / volume

# Cálculo do Erro do Inverso do Volume
erro_inverso_do_volume = erro_volume * inverso_do_volume ** 2

# Criando o DataFrame
df = pd.DataFrame({
    'V': volume,
    'σ_volume': erro_volume,
    '1/v': inverso_do_volume,
    'σ_1/V': erro_inverso_do_volume
})

# Formatação com tabulate
tabela_formatada = tabulate(df, headers='keys', tablefmt='grid', showindex=False, floatfmt=".4f")

# Exibindo a tabela formatada
print(tabela_formatada)


# Para Cálculo de MMQ
# Considere P_man como f(x) e o Inverso do Volume como x

p_man = np.array([0.02, 0.03, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])

linear = (np.sum(p_man)*np.sum(inverso_do_volume**2) - np.sum(inverso_do_volume)*np.sum(inverso_do_volume*p_man)) / (p_man.size*np.sum(inverso_do_volume**2)-np.sum(inverso_do_volume)**2)

angular = (p_man.size*np.sum(p_man*inverso_do_volume)-np.sum(p_man)*np.sum(inverso_do_volume))/(p_man.size*np.sum(inverso_do_volume**2)-np.sum(inverso_do_volume)**2)

print(f'A reta é {angular}x + {linear}')



# Criação do Gráfico