import json
from datetime import datetime
import numpy as np
from sklearn.ensemble import IsolationForest

# Lendo as transações do arquivo JSON
with open('transacoes.json') as f:
    transacoes = json.load(f)

# Separando os dados de cada transação em listas diferentes
idades = []
nomes = []
rendas = []
datas_horas = []
categorias = []
cidades = []
estados = []
valores = []

for transacao in transacoes:
    # Coletando dados do cliente
    cliente = transacao['cliente']
    idades.append(cliente['idade'])
    nomes.append(cliente['nome'])
    rendas.append(cliente['renda_mensal'])
    
    # Coletando dados da transação
    datas_horas.append(datetime.strptime(transacao['data_hora'], '%Y-%m-%d %H:%M:%S'))
    estabelecimento = transacao['estabelecimento']
    categorias.append(estabelecimento['categoria'])
    cidades.append(estabelecimento['cidade'])
    estados.append(estabelecimento['estado'])
    valores.append(transacao['valor'])

# Convertendo listas para numpy arrays
X = np.array(list(zip(idades, rendas, valores)))

# Criando modelo IsolationForest
modelo = IsolationForest(contamination='auto', random_state=42)
modelo.fit(X)

# Definindo horários suspeitos
horarios_suspeitos = [1, 2, 3, 4, 5]

# Criando dicionário para armazenar alertas
alertas = {}

# Verificando cada transação
for i, transacao in enumerate(transacoes):
    # Coletando dados do cliente
    cliente = transacao['cliente']
    idade = cliente['idade']
    renda = cliente['renda_mensal']
    nome = cliente['nome']
    
    # Coletando dados da transação
    data_hora = datetime.strptime(transacao['data_hora'], '%Y-%m-%d %H:%M:%S')
    estabelecimento = transacao['estabelecimento']
    categoria = estabelecimento['categoria']
    cidade = estabelecimento['cidade']
    estado = estabelecimento['estado']
    valor = transacao['valor']
    
    # Verificando se o horário da transação é suspeito
    hora = data_hora.hour
    if hora in horarios_suspeitos and (data_hora.date() not in datas_horas):
        alertas[i] = {'nome': nome, 'tipo': 'horario'}
    
    # Verificando se a transação é uma "outlier"
    desvios = modelo.predict(X) == -1
    desvio_padrao = np.std(X[desvios], axis=0)
    media = np.mean(X[desvios], axis=0)
    limiar_superior = media + 3 * desvio_padrao
    if valor > limiar_superior[-1]:
        if i not in alertas:
            alertas[i] = {'nome': nome, 'tipo': 'valor'}
        else:
            alertas[i]['tipo'] += ' e valor'

# Escrevendo alertas no arquivo JSON
with open('alertas1.json', 'w') as f:
    json.dump(alertas, f)
