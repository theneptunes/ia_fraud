import random_forest
import logistic_progression

#[253.54 True False False False True False False True False False]
# valor,cat_eletronicos,local_recife,local_camps,cat_comida,horario_tarde,horario_noite,ca
#localizacao, valor, periodo, categoria
predicted = random_forest('Campinas-SP', 2000,'Noite','Comida')
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")

predicted_LG = logistic_progression('Campinas-SP', 2000,'Noite','Comida')
if predicted_LG[0] == 0:
    print("OK")
else:
    print("FRAUDE")
