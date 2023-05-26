import streamlit as st
import pandas as pd
import calendar

@st.cache_data()
def load_data():
    df = pd.read_csv("data/filtered.csv")
    # Removendo o símbolo "$" e convertendo a coluna "Amount" para float
    df['Amount'] = df['Amount'].str.replace('$', '').astype(float)
    return df

def main():
    st.title("Transações de Cartão de Crédito")
    
    # Carregando os dados
    df = load_data()
    
    # Exibindo informações sobre fraudes
    st.subheader("Detecção de Fraudes")
    st.write("Total de Transações: ", len(df))
    num_fraudulent_transactions = df['Is Fraud?'].eq('Yes').sum()
    st.write("Número de transações fraudulentas:", num_fraudulent_transactions)
    fraud_percentage = (num_fraudulent_transactions / len(df)) * 100
    st.write("Taxa de fraudes:", round(fraud_percentage,2), "%")
    
    # Exibindo o dataframe
    st.subheader("Dados do Arquivo CSV")
    st.dataframe(df)
    
    # Filtrando por cartão
    all_cards_option = "Todos os Cartões"
    selected_card = st.sidebar.selectbox("Selecione um cartão", [all_cards_option] + list(df['Card'].unique()))
    if selected_card != all_cards_option:
        filtered_df_card = df[df['Card'] == selected_card]
    else:
        filtered_df_card = df
    
    # Filtrando por ano
    all_years_option = "Todos os Anos"
    selected_year = st.sidebar.selectbox("Selecione um ano", [all_years_option] + list(df['Year'].unique()))
    if selected_year != all_years_option:
        filtered_df_year = df[df['Year'] == selected_year]
    else:
        filtered_df_year = df
        
    # Exibindo informações do cartão selecionado
    st.sidebar.subheader("Informações do Cartão")
    st.sidebar.write("ID do Cartão:", selected_card)
    st.sidebar.write("Total de Transações no Cartão:", len(filtered_df_card))
    st.sidebar.write("Total de Transações no Ano:", len(filtered_df_year))
    
    # Exibindo gráfico de quantidade de transações por mês
    st.subheader("Transações por Mês")
    if selected_year != all_years_option and selected_card != all_cards_option:
        transactions_by_month = filtered_df_year[filtered_df_year['Card'] == selected_card].groupby('Month').size()
    elif selected_year != all_years_option:
        transactions_by_month = filtered_df_year.groupby('Month').size()
    elif selected_card != all_cards_option:
        transactions_by_month = filtered_df_card.groupby('Month').size()
    else:
        transactions_by_month = df.groupby('Month').size()
        
    if len(transactions_by_month) > 0:
        transactions_by_month.index = transactions_by_month.index.map(lambda x: calendar.month_abbr[x])
        st.line_chart(transactions_by_month)
    else:
        st.warning("Nenhum resultado encontrado com os filtros selecionados.")
    
    # Calculando e exibindo o total do valor das transações por ano
    st.subheader("Valor Total das Transações por Ano")
    transactions_by_year = filtered_df_card.groupby('Year')['Amount'].sum()
    st.bar_chart(transactions_by_year)
    
    # Exibindo informações adicionais da transação selecionada
    st.subheader("Detalhes da Transação")
    selected_transaction = st.selectbox("Selecione uma transação", filtered_df_card.index)
    transaction_details = filtered_df_card.loc[selected_transaction]
    st.write("Data:", transaction_details['Day'], "/", transaction_details['Month'], "/", transaction_details['Year'])
    st.write("Hora:", transaction_details['Time'])
    st.write("Valor:", transaction_details['Amount'])
    st.write("Estabelecimento:", transaction_details['Merchant Name'])
    st.write("Cidade:", transaction_details['Merchant City'])
    st.write("Estado:", transaction_details['Merchant State'])

if __name__ == '__main__':
    main()
