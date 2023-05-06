import pandas as pd
import json
import random

# Lê o arquivo JSON e carrega em uma lista
with open('transacoes.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Normaliza o JSON em um DataFrame
df = pd.json_normalize(dados)
grupos_clientes = df.groupby('cliente.nome')

std_por_cliente = df.groupby('cliente.nome')['valor'].std()
limite_superior = std_por_cliente * 4
media_por_cliente = df.groupby('cliente.nome')['valor'].mean()
mediana_por_cliente = df.groupby('cliente.nome')['valor'].median()
maximo_por_cliente = df.groupby('cliente.nome')['valor'].max()
valor_suspeito = df.apply(lambda row: row['valor'] > (std_por_cliente[row['cliente.nome']] * 4), axis=1)
horario_suspeito = df['data_hora'].apply(lambda x: True if int(x.split(' ')[1].split(':')[0]) >= 1 and int(x.split(' ')[1].split(':')[0]) <= 5 else False)

#Imprime os resultados
print("\nEstatísticas por cliente:")
print(std_por_cliente)
print(media_por_cliente)
print(mediana_por_cliente)
print(maximo_por_cliente)