import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

# Entrada em np arrays
class DadosExperimentais():
    def __init__(self, variavel_livre, erro_variavel_livre, variavel_dependente, erro_variavel_dependente):
        self.variavel_livre = variavel_livre
        self.erro_variavel_livre = erro_variavel_livre
        self.variavel_dependente = variavel_dependente
        self.erro_variavel_dependente = erro_variavel_dependente

    def criar_tabela(self):
        # Criando o DataFrame
        df = pd.DataFrame({
            'Ln(R/Ro)':   self.variavel_dependente,
            'σ_Ln(R/Ro)': self.erro_variavel_dependente,
            '1/T': self.variavel_livre,
            'σ_1/T': self.erro_variavel_livre,
        })
        # Formatação com tabulate
        tabela_formatada = tabulate(df, headers='keys', tablefmt='grid', showindex=False, floatfmt=".10f")

        # Exibindo a tabela formatada
        print(tabela_formatada)


class Linearizacao(DadosExperimentais):
    def __init__(self, variavel_livre, erro_variavel_livre, variavel_dependente, erro_variavel_dependente):
        self.variavel_livre = variavel_livre
        self.erro_variavel_livre = erro_variavel_livre
        self.variavel_dependente = variavel_dependente
        self.erro_variavel_dependente = erro_variavel_dependente

    # Pesos
    def weights(self):
        return 1 / (self.erro_variavel_dependente ** 2)  # Não é definido para erro nulo
    
    def sigma2(self):   
        return np.sum(self.weights())

    # Médias ponderadas
    def x_mean(self):
        return np.sum(self.variavel_livre * self.weights()) / self.sigma2()
    
    def x2_mean(self):
        return np.sum(self.variavel_livre ** 2 * self.weights()) / self.sigma2()
        
    
    def y_mean(self):
        return np.sum(self.variavel_dependente * self.weights()) / self.sigma2()
    
    def xy_mean(self):
        return np.sum(self.variavel_livre * self.variavel_dependente * self.weights()) / self.sigma2()
    

    # Coeficientes a e b
    def a(self):
        return (self.x_mean() * self.y_mean() - self.xy_mean()) / (self.x_mean() ** 2 - self.x2_mean())

    def b(self):
        return self.y_mean() - self.a() * self.x_mean()
    
    # Incertezas (Delta a e Delta b)
    def delta_a(self):
        return np.sqrt((1 / self.sigma2()) / (self.x2_mean() - self.x_mean() ** 2))
    
    def delta_b(self):
        return np.sqrt((self.x2_mean() / self.sigma2()) / (self.x2_mean() - self.x_mean() ** 2))
    
    def equacao(self):
        print(f'y = ({self.a()} +- {self.delta_a()})x + ({self.b()}+-{self.delta_b()})')

    def grafico(self, titulo, xlabel, ylabel, label):
        # Gera pontos para a reta ajustada
        x_fit = np.linspace(min(self.variavel_livre), max(self.variavel_livre), 100)
        y_fit = self.a() * x_fit + self.b()

        plt.rcParams['text.usetex'] = True
        plt.figure(figsize=(8.67,5.94))
        plt.errorbar(self.variavel_livre, self.variavel_dependente, xerr=self.erro_variavel_livre, yerr=self.erro_variavel_dependente, fmt='o', label='Pontos experimentais')
        plt.plot(x_fit, y_fit, 'r-', label=label)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(titulo)
        plt.legend()
        plt.grid()
        plt.subplots_adjust(left=0.14, right=0.92, bottom=0.15, top=0.90)
        plt.savefig("grafico.png", dpi=1000, bbox_inches='tight', pad_inches=1) 
        plt.show()

#### Dados desse Relatório

temperatura_celsius = np.array([27, 81, 74, 67, 62, 60, 51, 45, 41, 37, 34])
erro_temperatura = np.array(11*[1])
resistencia = np.array([42, 3.72, 5.02, 6.59, 8.28, 9.32, 13.59, 17.07, 20.84, 24.56, 25.70])
erro_resistencia = np.array([
    resistencia[i] * 0.012 + 4 * 10 **(-3)* (1 if resistencia[i] < 4 else (10 if 4 <= resistencia[i] <= 40 else 100)) for i in range(len(resistencia))
])

#### Dados Processados

inverso_temperatura_kelvin = 1/(temperatura_celsius[1:] + 273)

erro_inverso_temperatura_kelvin = erro_temperatura[1:] * inverso_temperatura_kelvin ** 2


logaritmo = np.log(resistencia[1:]/resistencia[0])

erro_logaritmo = np.sqrt((erro_resistencia[1:] /resistencia[1:])**2 + (erro_resistencia[0]/resistencia[0])**2)



relatorio2 = DadosExperimentais(logaritmo, erro_logaritmo,inverso_temperatura_kelvin, erro_inverso_temperatura_kelvin)

linearizacao1 = Linearizacao(
    relatorio2.variavel_livre,
    relatorio2.erro_variavel_livre,
    relatorio2.variavel_dependente,
    relatorio2.erro_variavel_dependente
)

linearizacao1.grafico(
    f"Gráfico de $\\frac{{1}}{{T}}$ por $\\ln\\bigg( \\frac{{R}}{{R_0}} \\bigg)$",
    r"$\ln \bigg( \frac{R}{R_0} \bigg)$",
    r"$\frac{1}{T}\quad (K^{-1})$", 
    f'Ajuste: $y = \\big[({10**4*linearizacao1.a():.2f} \pm {10**4*linearizacao1.delta_a():.2f})\\times 10^{{-4}} x + ({10**3*linearizacao1.b():.3f} \pm {10**3*linearizacao1.delta_b():.3f})\\times 10^{{-3}}\\big] K^{{-1}}$'
    )

