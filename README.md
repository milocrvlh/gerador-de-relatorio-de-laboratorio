# 𝔾𝕖𝕣𝕒𝕕𝕠𝕣 𝕕𝕖 ℝ𝕖𝕝𝕒𝕥𝕠́𝕣𝕚𝕠 𝕕𝕖 𝕃𝕒𝕓𝕠𝕣𝕒𝕥𝕠́𝕣𝕚𝕠

# Objetivos
O código tem a finalidade de:

-Fazer uma tabela dos dados experimentais fornecidos;
-Calcular os pesos e parâmetros do Método dos Mínimos Quadrados Ponderados, podendo gerar um arquivo em latex com essas informações;
-O gráfico da reta que melhor aproxima os pontos experimentais.


# Requerimentos
Necessário ter instalado Python - preferencialmente 3.11.9 - e as seguintes bibliotecas:

contourpy==1.3.1
cycler==0.12.1
fonttools==4.56.0
kiwisolver==1.4.8
matplotlib==3.10.0
mpmath==1.3.0
numpy==2.2.2
packaging==24.2
pandas==2.2.3
pillow==11.1.0
pyparsing==3.2.1
python-dateutil==2.9.0.post0
pytz==2025.1
six==1.17.0
sympy==1.13.3
tabulate==0.9.0
tzdata==2025.1

Além disso, é necessário possuir algum ambiente que rode o Latex. Sugiro o TeX Live para melhor compatibilidade com o português.

# Como usar

Para usar o gerador, é necessário, no arquivo 'gerador_de_relatorio.py', instanciar uma das classes com os dados experimentais e utilizar a função requerida.


# Ideias futuras

- Implementação do cálculo de erros com derivadas usando Sympy;
- Interface gráfica com Custom TKinter.

# Show off
Arquivo gerado com pesos e parâmetros do Método dos Mínimos Quadrados Ponderados
[wls.pdf](https://github.com/user-attachments/files/19479670/wls.pdf)

Gráfico gerado com dados experimentais
![grafico](https://github.com/user-attachments/assets/dcf043e3-9951-407d-aa5d-fd0c652045ed)

Tabela gerada com dados experimentais
![tabela_gerada](https://github.com/user-attachments/assets/9159cd0a-99cf-40fe-9614-fa59b2d4095a)
