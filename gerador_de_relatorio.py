import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Entrada em np arrays
class DadosExperimentais():
    def __init__(self, variavel_livre, erro_variavel_livre, variavel_dependente, erro_variavel_dependente):
        self.variavel_livre = variavel_livre
        self.erro_variavel_livre = erro_variavel_livre
        self.variavel_dependente = variavel_dependente
        self.erro_variavel_dependente = erro_variavel_dependente

    def criar_tabela(self):
        # Criando o DatFrame
        df = pd.DataFrame({
            'P_man':   self.variavel_dependente,
            'σ_p_man': self.erro_variavel_dependente,
            '1/h': self.variavel_livre,
            'σ_1/h': self.erro_variavel_livre,
        })
        # Formatação com tabulate
        tabela_formatada = tabulate(df, headers='keys', tablefmt='grid', showindex=False, floatfmt=".4f")

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
        plt.rcParams['text.usetex'] = True
        plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
        # --- 1. Configuração inicial ---
        fig, ax = plt.subplots(figsize=(9, 6.5)) # Proporção próxima de 9x6

        # --- Plotagem dos dados ---
        x_fit = np.linspace(min(self.variavel_livre), max(self.variavel_livre), 100)
        y_fit = self.a() * x_fit + self.b()

        ax.errorbar(self.variavel_livre, self.variavel_dependente,
                    xerr=self.erro_variavel_livre, yerr=self.erro_variavel_dependente,
                    fmt='o', color='black', ecolor='gray', capsize=2, zorder=10, label='Pontos experimentais')
        ax.plot(x_fit, y_fit, 'r-', zorder=5, label=label)

        # --- 2. Lógica da Grade Personalizada (9x6 quadrados) ---
        # Defina o espaçamento FIXO e "arredondado" para as grades.
        major_spacing_x = 0.01
        minor_spacing_x = 0.001  # 1/10 do principal
        major_spacing_y = 0.1
        minor_spacing_y = 0.01   # 1/10 do principal

        # Aplica as marcações com base no espaçamento fixo
        ax.xaxis.set_major_locator(ticker.MultipleLocator(major_spacing_x))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(minor_spacing_x))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(major_spacing_y))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(minor_spacing_y))

        # Estiliza a grade
        ax.grid(which='major', color='#B22222', linestyle='-', linewidth=0.7)
        ax.grid(which='minor', color='#FA8072', linestyle=':', linewidth=0.5)

        # --- 3. Configurações finais e LIMITES MANUAIS ---
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(titulo)
        ax.legend()

        # Define os limites dos eixos MANUALMENTE para criar a grade 9x6
        ax.set_xlim(0.06, 0.15)  # 9 seções de 0.01 (0.15 - 0.06 = 0.09)
        ax.set_ylim(0, 0.6)      # 6 seções de 0.1  (0.6 - 0.0 = 0.6)

        fig.tight_layout()
        plt.savefig("grafico_milimetrado_9x6.png", dpi=300)
        plt.show()


    def gerar_relatorio_latex_wls(self, fmt=".5f"):
        # Função auxiliar para formatar os números para LaTeX
        def format_latex(numero):
            # Formata em notação científica padrão do Python (ex: 1.23456e+02)
            num_str = f"{numero:.5e}"
            # Substitui 'e' pela sintaxe LaTeX
            if 'e' in num_str:
                base, expoente = num_str.split('e')
                # Retorna no formato LaTeX: 1.23456 \times 10^{2}
                return fr"{float(base):{fmt}} \times 10^{{{int(expoente)}}}"
            return f"{numero:{fmt}}"

        latex_template = """% !TeX root = wls.tex
        \\documentclass[12pt]{{article}} % Especifica o tamanho da fonte

        %%----------------PACOTES-------------------------------------------%%
        \\usepackage[a4paper,margin=1in]{{geometry}} % Define todas as margens em 1 polegada
        \\usepackage{{graphicx}} % Permite a inclusão de arquivos de imagem
        \\usepackage{{amsmath}} % Permite o uso de símbolos matemáticos avançados
        \\usepackage{{amssymb}} % Permite o uso de símbolos matemáticos
        %%-----------FORMATAÇÃO----------------------------------------------%%

        %%-------------------------------------------------------------------%%

        \\begin{{document}}

        {conteudo}

        \\end{{document}}
        """

        # Gera a lista de pesos já formatada para LaTeX
        latex_weights = " \\\\\n".join(
            [fr"$\frac{{1}}{{\sigma^2_{{{i}}}}} = {format_latex(weight)}$"
             for i, weight in enumerate(self.weights(), start=1)]
        )

        # Gera o conteúdo principal, incluindo o gráfico
        conteudo = fr"""
        \section*{{Resultado do WLS}}

        \subsubsection*{{Pesos}}
        {latex_weights}
        
        \subsection*{{Parâmetros}}
        $\langle\sigma^2\rangle = {format_latex(self.sigma2())}$
        
        $\langle x \rangle = {format_latex(self.x_mean())}$
        
        $\langle x^2 \rangle = {format_latex(self.x2_mean())}$
        
        $\langle y \rangle = {format_latex(self.y_mean())}$
        
        $\langle xy \rangle = {format_latex(self.xy_mean())}$
        
        $a = {format_latex(self.a())}$
        
        $b = {format_latex(self.b())}$
        
        $\Delta a = {format_latex(self.delta_a())}$
        
        $\Delta b = {format_latex(self.delta_b())}$
        """

        # Escreve no arquivo
        with open("wls.tex", 'w', encoding='utf-8') as f:
            f.write(latex_template.format(conteudo=conteudo))



#### Dados desse Relatório

p_man = np.array([0.56, 0.49, 0.40, 0.33, 0.26, 0.20, 0.14, 0.11, 0.06])
erro_man = np.array(len(p_man)*[0.005])
h = np.array([i for i in range(7,16)])
erro_h= np.array(len(h)*[0.5])

#### Dados Processados

inverso_h = 1/h
erro_inverso_h = erro_h / h**2 

################
relatorio2 = DadosExperimentais(inverso_h, erro_inverso_h, p_man, erro_man)
 
linearizacao1 = Linearizacao(
    relatorio2.variavel_livre,
    relatorio2.erro_variavel_livre,
    relatorio2.variavel_dependente,
    relatorio2.erro_variavel_dependente
)

linearizacao1.grafico(
    f"Grafico",
    r"variavel livre",
    r"variavel dependente", 
    f'Ajuste: $y = \\big[({10**4*linearizacao1.a():.2f} \\pm {10**4*linearizacao1.delta_a():.2f})\\times 10^{{-4}} x + ({10**3*linearizacao1.b():.3f} \\pm {10**3*linearizacao1.delta_b():.3f})\\times 10^{{-3}}\\big] K^{{-1}}$'
)

# linearizacao1.gerar_relatorio_latex_wls()
# linearizacao1.criar_tabela()


