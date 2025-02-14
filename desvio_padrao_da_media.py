import numpy as np


# Recolher dados experimentais do usuários
dados = [float(i) for i in input("Insira uma lista de dados: ").split()]


# Calcula a média e desvio padrão da média
dados = np.array(dados)

media = np.mean(dados)

def desvio_padrao_da_media(dados, media):
    return np.sqrt((1/(dados.size*(dados.size-1)))*np.sum((dados-media)**2))

print(f"A média é {media}")
print(f"A incerteza é {desvio_padrao_da_media(dados, media)}")