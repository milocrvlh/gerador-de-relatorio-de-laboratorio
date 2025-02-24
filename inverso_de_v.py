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



