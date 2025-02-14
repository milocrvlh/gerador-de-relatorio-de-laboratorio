
# Entrada do usuário
entrada = float(input(" Insira a entrada da medida: "))
err = float(input(" Insira o erro da medida: "))

# Erro e média com abordagem primitiva
# Generalizar com simpy no futuro
min = (entrada - err) ** 2
max = (entrada + err) ** 2

media = (max + min)/2
err_primitivo = (max - min)/2

# Implementar classes
# Erro e média com derivada

media_derivada = entrada ** 2
err_derivada = abs(2 * entrada) * 0.05

print("Mínimo: ", min)
print("Máximo: ", max)
print(f"Com a abordagem primitiva, temos: {media} +- {err_primitivo}")
print(f"Com a abordagem da derivada, temos: {media_derivada} +- {err_derivada}")

