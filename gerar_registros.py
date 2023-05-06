import random

# Lista de categorias de compra
categorias = ['Comida', 'Lazer', 'Eletronicos', 'Moda', 'Saude']

# Gera aleatoriamente 5 transações
for i in range(5):
    # Nome completo fixo
    nome = 'Fernando Souza'
    
    # Localização com 70% de chance de ser Recife-PE
    if random.random() < 0.7:
        localizacao = 'Recife-PE'
    else:
        localizacao = 'Outra cidade'
    
    # Valor de transação entre 2000 e 5000
    valor = round(random.uniform(2000, 5000), 2)
    
    # Horário aleatório no formato HH:mm:ss
    horario = '{:02d}:{:02d}:{:02d}'.format(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    
    # Categoria de compra com 70% de chance de ser Eletronicos
    if random.random() < 0.7:
        categoria = 'Eletronicos'
    else:
        categoria = random.choice(categorias)
    
    # Imprime os valores separados por vírgula
    print(nome + ',' + localizacao + ',' + str(valor) + ',' + horario + ',' + categoria)
