from faker import Faker
import random
import json
from datetime import datetime, date, timedelta
import pymongo

# String de conexão do MongoDB
mongo_url = 'mongodb+srv://leo:123@cluster0.nknwieb.mongodb.net/?retryWrites=true&w=majority'
# Nome da coleção onde serão inseridos os documentos
collection_name = 'transactions'
# Nome do arquivo JSON que será carregado
json_file = '../transacoesLIGHT.json'
# Conexão com o MongoDB
client = pymongo.MongoClient(mongo_url)
# Banco de dados onde serão inseridos os documentos
db = client.get_database('pyredis')
# Coleção onde serão inseridos os documentos
collection = db[collection_name]

fake = Faker('pt_BR')

# define o horário mínimo como 5:00 AM
horario_minimo = datetime.strptime('05:00:00', '%H:%M:%S').time()

# define o horário máximo como 11:59 PM
horario_maximo = datetime.strptime('23:59:00', '%H:%M:%S').time()

# Gerando uma data aleatória entre um ano atrás e hoje
dias_atras = 365
data_inicial = datetime.today() - timedelta(days=dias_atras)
data_final = datetime.today()
delta = data_final - data_inicial
random_data = data_inicial + timedelta(days=random.randint(0, delta.days))
data_maxima = datetime.now() - timedelta(days=365)
start_date = date(2022, 4, 3)
end_date   = date.today()



clients = [{'nome': fake.name(),
             'estado_civil': random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viuvo']),
             'renda_mensal': round(random.uniform(1300.0, 10000.0), 2),
             'idade': random.randint(18, 80),
            'cidade': fake.city(),
            'estado': fake.state()} for i in range(10)]

transactions = []

print(len(clients))
for client in clients:
    for j in range(255):
        num_days   = (end_date - start_date).days
        rand_days   = random.randint(1, num_days)
        random_date = start_date + timedelta(days=rand_days)
        print("Random date")
        print(random_date)
        random_time = datetime.combine(random_date, horario_minimo) + timedelta(
        seconds=random.randint(0, int((datetime.combine(random_date, horario_maximo) -
                                     datetime.combine(random_date, horario_minimo)).total_seconds())))
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
        transaction['cliente'] = {}
        transaction['cliente']['nome'] = client['nome']
        transaction['cliente']['idade'] = client['idade']
        transaction['cliente']['renda_mensal'] = client['renda_mensal']

        transactions.append(transaction)

# Salvando as transações em um arquivo JSON
with open('transacoesLIGHT.json', 'w') as f:
    json.dump(transactions, f, indent=4, sort_keys=True, ensure_ascii=True)
# Carrega o arquivo JSON
with open(json_file, 'r') as f:
    data = json.load(f)

# Insere os documentos na coleção
collection.delete_many({})
result = collection.insert_many(data)

# Imprime o número de documentos inseridos
print(f'{len(result.inserted_ids)} documentos inseridos com sucesso na coleção {collection_name}')
