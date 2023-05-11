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
# Sendo i cada índice na tabela
for i in data.columns:

    # Caso i não esteja nas colunas numéricas (excluindo elas por enquanto)
    if i not in numeric_columns:

        # Inicializa a chave i (índice atual) do total como um objeto vazio
        infos['total'][i] = {}

        # Faz o mesmo para as probabilidades de sim e não
        infos['probability']['Yes'][i] = {}
        infos['probability']['No'][i] = {}

        # Sendo j um número que passará por todos os dados
        for j in range(len(data)):

            # Caso o valor na linha j e na coluna i (índice atual) não esteja no objeto dos totais ainda
            if str(data[i][j]) not in infos['total'][i]:

                # Cria esses índices onde a chave é o valor que está na posição atual na tabela e começa com 0
                infos['total'][i][str(data[i][j])] = 0

                # Faz o mesmo para as probabilidades de sim e não
                infos['probability']['Yes'][i][str(data[i][j])] = 0
                infos['probability']['No'][i][str(data[i][j])] = 0
            
# Preenche todos os dados contendo o total de ocorrências de cada um
# Sendo i um número que passará por todos os dados
for i in range(len(data)):

    # Sendo j cada uma das chaves do total de informações (colunas exceto numéricas)
    for j in infos['total']:

        # Soma 1 no total do valor da chave do elemento atual na tabela
        infos['total'][j][str(data[j][i])] += 1

        # Faz o mesmo na probabilidade, mas adiciona no Yes ou No dependendo do valor da coluna do elemento atual (se for Yes vai no Yes, se for No vai no No)
        infos['probability'][data[target][i]][j][str(data[j][i])] += 1

# Divide o total de casos específicos pelo total correspondente, obtendo as probabilidades em todos os casos (dado sim ou não para as fraudes)
# Sendo i cada uma das chaves do total de informações (colunas exceto numéricas)
for i in infos['total']:

    # Sendo j cada uma das chaves dentro da chave equivalente às colunas, que são as chaves que representam o quanto cada valor apareceu
    for j in infos['total'][i]:

        # Executa a operação para calcular a probabilidade tanto no Yes quanto no No. Dividindo o número de Yes pelo total, e o No pelo total.
        infos['probability']['Yes'][i][j] = infos['probability']['Yes'][i][j] / infos['total'][i][j]
        infos['probability']['No'][i][j] = infos['probability']['No'][i][j] / infos['total'][i][j]

# Printa o dicionário final
# print(infos)

# Função que recebe dados em dicionário dos valores do novo registro a ser previsto
def calculate(input_data):

    # Cria 'columns' que é basicamente uma lista das colunas exceto a última (que é a própria coluna de Is Fraud? com os Yes e No)
    columns = data.columns.tolist()
    columns.pop()

    # Sendo i cada um dos valores no columns (todas as colunas exceto a de Fraude)
    for i in columns:

        # Caso i não esteja nas colunas numéricas (excluindo elas por enquanto)
        if i not in numeric_columns:

            # Caso não haja o valor informado da coluna atual nas informações guardadas (seja um valor novo)
            if str(input_data[i]) not in infos['total'][i]:

                # Retorna -1 equivalente a erro
                return -1
    
    # Inicializa as probabilidades de ser Sim ou Não como 1 (já que vamos multiplicar várias probabilidades)
    probability = {
        'Yes': 1,
        'No': 1
    }

    # Sendo i Yes e depois No
    for i in ['Yes', 'No']:

        # Sendo j cada um dos valores no columns (todas as colunas exceto a de Fraude)
        for j in columns:

            # Caso j não esteja nas colunas numéricas (excluindo elas por enquanto)
            if j not in numeric_columns:

                # Printa a probabilidade para fins de enxergar o que está acontecendo
                print(i + ' ' + str(infos['probability'][i][j][str(input_data[j])]))
                
                # Multiplica a probabilidade atual desse caso pela probabilidade atual
                probability[i] *= infos['probability'][i][j][str(input_data[j])]
    
    # Printa as duas probabilidades finais
    print(probability)

    # Retorna 'Yes' caso a probabilidade do Yes seja maior, ou 'No' caso contrário
    return 'Yes' if probability['Yes'] > probability['No'] else 'No'

# Printa o retorno da função calculate passando um parâmetro exemplo
print(calculate({
    'User': 1,
    'Card': 0,
    'Year': 2015,
    'Month': 11,
    'Day': 15,
    'Use Chip': 'Online Transaction',
    'Merchant Name': '-8194607650924472520',
    'Merchant City': 'ONLINE',
    'Merchant State': 'nan',
    'Zip': 'nan',
    'MCC': 3001,
    'Errors?': 'nan'
}))