import numpy as np



dados = list()

# Recolher dados experimentais do usuários
while True:
    dados.append(float(input("Insira uma medição: ")))
    continuar = input("Continuar inserindo dados? S/N ")
    if continuar == "N":
        break

# Calcula a média e desvio padrão da média
dados = np.array(dados)

media = np.mean(dados)

def desvio_padrao_da_media(dados, media):
    return np.sqrt((1/(dados.size*(dados.size-1)))*np.sum((dados-media)**2))

print(f"A média é {media}")
print(f"A incerteza é {desvio_padrao_da_media(dados, media)}")