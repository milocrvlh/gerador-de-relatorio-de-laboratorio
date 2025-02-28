import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

### INPUT DE DADOS
# Dados da Pressão Manométrica
p_man = np.array([0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])

# Dados de erro da Pressão Manométrica 
p_man_erro = np.array([0.005]*9)


# Dados de Volume do laboratório
volume = np.array([17., 15.5, 14.5, 13.5, 12.5, 11.5, 10.5, 10.0, 9.5]) + 9.5

# Dados do Erro do Volume do laboratório
erro_volume = np.array([0.5]*9)



### PROCESSAMENTO DE DADOS

# Cálculo do Inverso do Volume
inverso_do_volume = 1 / volume

# Cálculo do Erro do Inverso do Volume
erro_inverso_do_volume = erro_volume * inverso_do_volume ** 2


def weighted_least_squares(x, y, sigma):
    """
    Calcula os coeficientes a, b e suas incertezas usando o método WLE
    """
    # Pesos: 1/sigma_i^2

    weights = 1 / (sigma ** 2)
    sum_weights = np.sum(weights)
    

    # Médias ponderadas
    x_mean = np.sum(x * weights) / sum_weights
    x2_mean = np.sum(x ** 2 * weights) / sum_weights
    y_mean = np.sum(y * weights) / sum_weights
    xy_mean = np.sum(x * y * weights) / sum_weights
    
    # Coeficientes a e b
    a = (x_mean * y_mean - xy_mean) / (x_mean ** 2 - x2_mean)
    b = y_mean - a * x_mean
    
    # Incertezas (Delta a e Delta b)
    delta_a = np.sqrt((1 / sum_weights) / (x2_mean - x_mean ** 2))
    delta_b = np.sqrt((x2_mean / sum_weights) / (x2_mean - x_mean ** 2))
    print(f'<sigma> = {sum_weights}\n<x> ={x_mean}\n<x^2>={x2_mean}\n<y>={y_mean}\n<xy>={xy_mean}')
    return a, b, delta_a, delta_b
    
# Ajuste dos dados
a, b, delta_a, delta_b = weighted_least_squares(inverso_do_volume, p_man, p_man_erro)

# Gera pontos para a reta ajustada
x_fit = np.linspace(min(inverso_do_volume), max(inverso_do_volume), 100)
y_fit = a * x_fit + b

### GRÁFICO - Pressão Manométrica pelo Inverso do Volume

plt.rcParams['text.usetex'] = True
plt.figure()
plt.errorbar(inverso_do_volume, p_man, xerr=erro_inverso_do_volume, yerr=p_man_erro, fmt='o', label='Dados com erros')
plt.plot(x_fit, y_fit, 'r-', label=f'Ajuste: $y = ({a:.1f} \pm {delta_a:.1f})x + ({b:.2f} \pm {delta_b:.2f})$')
plt.xlabel(r"$\frac{1}{V}\quad (mL^{-1})$")
plt.ylabel(r"$P_{man} \quad(kgf/cm^2)$")
plt.title("Pressão Manométrica pelo Inverso do Volume")
plt.legend()
plt.grid()
plt.savefig("grafico1.png")
plt.show()

#### PARTE 2

volumeSI = volume * 10 ** (-6)
erro_volumeSI = erro_volume * 10 ** (-6)
p_atmSI = (-b) * 9.8 * 10**4
p_atm_erroSI = (delta_b) * 9.8 * 10 **4
p_manSI = p_man * 9.8 * 10 **4
p_man_erroSI = p_man_erro * 9.8 * 10 **4

p_totSI = (p_manSI + p_atmSI) 
p_totVSI = p_totSI * volumeSI

erro_p_totVSI = np.sqrt((volumeSI**2)*(p_man_erroSI**2+p_atm_erroSI**2) + (p_totSI**2)*(erro_volumeSI**2))

### GRÁFICO - Pressão total vezes Volume

plt.rcParams['text.usetex'] = True
plt.figure()
plt.errorbar(volumeSI, p_totVSI, xerr=erro_volumeSI, yerr=erro_p_totVSI, fmt='o', label='Dados com erros')
#plt.plot(x_fit, y_fit, 'r-', label=f'Ajuste: $y = ({a:.1f} \pm {delta_a:.1f})x + ({b:.2f} \pm {delta_b:.2f})$')
plt.xlabel(r"$\frac{1}{V}\quad (m^3)$")
plt.ylabel(r"$P_{man} \quad(Pa)$")
plt.title("Pressão Total X Volume")
plt.legend()
plt.grid()
plt.savefig("grafico2.png")
plt.show()


# Criando o DataFrame
df = pd.DataFrame({
    'P_man': p_man,
    'σ_P_man':p_man_erro,
    'V': volume,
    'σ_volume': erro_volume,
    '1/v': inverso_do_volume,
    'σ_1/V': erro_inverso_do_volume,
    'P_tot * V': p_totVSI,
    'σ_(P_tot * V)': erro_p_totVSI

})

# Formatação com tabulate
tabela_formatada = tabulate(df, headers='keys', tablefmt='grid', showindex=False, floatfmt=".4f")

# Exibindo a tabela formatada
print(tabela_formatada)

#### Exercício da Constante
print(f"P_tot * V = {np.mean(p_totVSI)} +- {np.std(p_totVSI)/np.sqrt(p_totVSI.size)}")

#### Exercício de Mols
R = 8.371
alpha = a * 0.098
err_alpha = delta_a * 0.098
T = 26.5 + 273
err_T = 0.5

print(f'n = {alpha/(T*R)} +- {(err_alpha/(R*T))**2 + (alpha*(err_T)**2)/(R*T**2)}')


### Exercício de R
k = np.mean(p_totVSI)
k_err = np.std(p_totVSI)/np.sqrt(p_totVSI.size)

n = alpha/(T*R)
n_err = (err_alpha/(R*T))**2 + (alpha*(err_T)**2)/(R*T**2)

r_ = k / (n*T)
r_err = np.sqrt((k_err/(n*T))**2+((k*n_err/T)**2)/n**4+((k*err_T/n)**2)/T**4)                 

print(f"R = {r_}+-{r_err}")