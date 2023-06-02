import streamlit as st
import datetime
import lgbm


def search_data(year: int, month: int, day: int, time: float, amount: float, use_chip: int, merchant_name: int, merchant_city: int):
    predicted = lgbm([[year, month, day, time, amount, use_chip, merchant_name, merchant_city]])
    if predicted[0] == 0:
        result = "OK"
    else:
        result = "FRAUDE"
    return result

def main():
    # Create input fields
    st.title('Data Search')


    result = st.empty()

    year = st.number_input('Ano da Transação', min_value=0, value=2022, max_value=2023)
    month = st.number_input('Mes da Transação', min_value=1, value=1, max_value=12)
    day = st.number_input('Dia da Transação', min_value=0, value=15, max_value=31)
    time = st.number_input('Hora da Transação', min_value=0, value=12, max_value=24)
    amount = st.number_input('Valor da Transação', min_value=0.0, value=42.0)
    use_chip = st.number_input('Tipo da Transação')
    merchant_name = st.number_input('Nome do Estabelecimento')
    merchant_city = st.number_input('Cidade da Transação')

    botao = st.button('Search')

    # Search button
    if botao:
        result_text = search_data(year, month, day, time, amount, use_chip, merchant_name, merchant_city)
        col1, col2, col3 = st.columns(3)
        col1.metric("", result_text, "")
    
if __name__ == '__main__':
    main()