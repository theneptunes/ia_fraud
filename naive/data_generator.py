from faker import Faker
import random
import json
from datetime import datetime, date, timedelta
import os
import pandas as pd

# Gera uma data aleatória
def gen_random_date(min = date.today() - timedelta(days=365), max = date.today()):
    days_diff = (max - min).days
    rand_days = random.randint(0, days_diff)
    return min + timedelta(days=rand_days)

def flatten_data(json):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(json)
    return out

# Nome do arquivo JSON que salvo
json_file = 'transactions.json'

# Nome da pasta
folder = './data/'

# Caminho onde o arquivo será salvo
path = folder + json_file

# Inicializando o Faker
fake = Faker('pt_BR')

# define o horário mínimo como 5:00 AM
min_time = datetime.strptime('05:00:00', '%H:%M:%S').time()

# define o horário máximo como 11:59 PM
max_time = datetime.strptime('23:59:00', '%H:%M:%S').time()

# Definindo o range de datas para serem geradas
start_date = date(2022, 4, 3)
end_date   = date.today()

# Gera os clientes
clients = [{'nome': fake.name(),
            'estado_civil': random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viuvo']),
            'renda_mensal': round(random.uniform(1300.0, 10000.0), 2),
            'idade': random.randint(18, 80),
            'cidade': fake.city(),
            'estado': fake.state()} for i in range(10)]

transactions = []

# Gera as transações, sendo 255 por cliente
for client in clients:
    for j in range(255):
        print("Random date")
        random_date = gen_random_date(start_date, end_date)
        print(random_date)
        random_time = datetime.combine(random_date, min_time) + timedelta(
        seconds=random.randint(0, int((datetime.combine(random_date, max_time) -
                                     datetime.combine(random_date, min_time)).total_seconds())))
        transaction = {}
        transaction['id_transacao'] = fake.uuid4()
        transaction['valor'] = round(random.SystemRandom().uniform(1, 2000), 2)
        
         # Gerando um horário aleatório entre 5:00 AM e 11:59 PM
        transaction['data_hora'] = random_time.strftime('%Y-%m-%d %H:%M:%S')

        # Gerando informações aleatórias sobre o estabelecimento
        transaction['estabelecimento'] = {}
        transaction['estabelecimento']['categoria'] = random.choice(['Varejo', 'Restaurante', 'Supermercado', 'Online'])

        if random.random() < 0.5:
            # Estabelecimento na mesma cidade do cliente
            transaction['estabelecimento']['cidade'] = client['cidade']
            transaction['estabelecimento']['estado'] = client['estado']
        else:
            # Estabelecimento no mesmo estado do cliente, mas diferente cidade
            transaction['estabelecimento']['cidade'] = fake.city()
            transaction['estabelecimento']['estado'] = client['estado']

        # Atribuindo o nome do cliente e os dados do cartão de crédito
        transaction['cliente'] = {
            'nome': client['nome'],
            'idade': client['idade'],
            'renda_mensal': client['renda_mensal'],
        }

        transactions.append(transaction)

# Verifica se existe o caminho para escrever o arquivo, se não existir ele cria
if not os.path.exists(folder):
    os.makedirs(folder)

# Salvando as transações em um arquivo JSON
with open(path, 'w') as f:
    json.dump(transactions, f, indent=4, sort_keys=True, ensure_ascii=True)