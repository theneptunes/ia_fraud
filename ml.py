import pandas as pd
import numpy as np
import json
from sklearn.ensemble import IsolationForest

# Lê o arquivo JSON e carrega em uma lista
with open('transacoes.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Normaliza o JSON em um DataFrame
df = pd.json_normalize(dados)

dados_por_cliente = df.groupby('cliente').mean()

# Treina o modelo de detecção de anomalias com o Isolation Forest
modelo = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.1, random_state=0)
modelo.fit(dados_por_cliente[['media_gastos']])

# Simula uma nova transação com um valor de gasto acima do normal
cliente_novo = 'João da Silva'
valor_gasto_novo = 5000
dados_novo = {'cliente': cliente_novo, 'valor': valor_gasto_novo}
df_novo = pd.DataFrame([dados_novo])

# Agrupa os dados por cliente e calcula a média de gastos por cliente novamente
dados_por_cliente_novo = pd.concat([df, df_novo]).groupby('cliente').mean()

# Verifica a média de gastos do novo cliente
media_gastos_novo = dados_por_cliente_novo.loc[cliente_novo]['media_gastos']

# Simula a nova transação como um DataFrame
transacao_nova = pd.DataFrame([[media_gastos_novo, valor_gasto_novo]])

# Detecta a anomalia na nova transação
resultado = modelo.predict(transacao_nova)
if resultado[0] == -1:
    print(f"Alerta de transação suspeita para o cliente {cliente_novo}!")
else:
    print(f"Transação normal para o cliente {cliente_novo}.") 
