import pandas as pd

# Define onde está a base de dados em csv
path = 'User0_credit_card_transactions.csv'
# Define a variável data como sendo o data frame importado do csv
data = pd.read_csv(path)
# Define target (a coluna que queremos prever)
target = 'Is Fraud?'

# Inicializa infos que será o dicionário que conterá todas as informações de probabilidades
infos = dict()
# Define as colunas numéricas que serão deixadas de lado por enquanto
numeric_columns = ['Time', 'Amount']

# Inicializa infos
infos['total'] = {}
infos['probability'] = {
    'Yes': {},
    'No': {}
}

# Cria um campo contendo o valor zero para cada valor diferente que for encontrado nas colunas
for i in data.columns:
    if i not in numeric_columns:
        infos['total'][i] = {}
        infos['probability']['Yes'][i] = {}
        infos['probability']['No'][i] = {}
        for j in range(len(data)):
            if str(data[i][j]) not in infos['total'][i]:
                infos['total'][i][str(data[i][j])] = 0
                infos['probability']['Yes'][i][str(data[i][j])] = 0
                infos['probability']['No'][i][str(data[i][j])] = 0
            
# Preenche todos os dados contendo o total de ocorrências de cada um
for i in range(len(data)):
    for j in infos['total']:
        infos['total'][j][str(data[j][i])] += 1
        infos['probability'][data[target][i]][j][str(data[j][i])] += 1

# Divide o total de casos específicos pelo total correspondente, obtendo as probabilidades em todos os casos (dado sim ou não para as fraudes)
for i in infos['total']:
    for j in infos['total'][i]:
        infos['probability']['Yes'][i][j] = infos['probability']['Yes'][i][j] / infos['total'][i][j]
        infos['probability']['No'][i][j] = infos['probability']['No'][i][j] / infos['total'][i][j]

# Printa o dicionário final
print(infos)

# TODO: Fazer uma função que recebe parâmetros de uma nova transação (excluindo os numéricos) e usa o Naive Bayes com as probabilidades para determinar se é Fraude ou não