#!/bin/bash

echo "Gerando dados e gráfico com Python"
python gerador_de_relatorio.py 

echo "Compilando o relatório com pdflatex"
pdflatex wls.tex

echo "Compilação concluída! Verifique o arquivo wls.pdf"