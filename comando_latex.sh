#!/bin/bash

echo "Gerando Exercícios"
python gerador_de_relatorio

echo "Parafernalha do Latex"
latex wls.tex
dvipdfm wls.dvi
