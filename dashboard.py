import streamlit as st
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import json

def main():
    st.title("Transações de Cartão de Crédito")

    # Carregando os dados
    df = pd.read_csv('data/transactions_final.csv')

    # Convertendo a coluna "Month" para tipo int
    df['Month'] = df['Month'].astype(int)

    # Removendo o símbolo "$" e convertendo a coluna "Amount" para float
    df['Amount'] = df['Amount'].astype(str).str.replace('$', '').astype(float)

    # Exibindo informações sobre fraudes
    st.subheader("Detecção de Fraudes")
    st.write("Total de Transações:", len(df))
    num_fraudulent_transactions = df['Is Fraud'].sum()
    st.write("Número de transações fraudulentas:", num_fraudulent_transactions)
    fraud_percentage = (num_fraudulent_transactions / len(df)) * 100
    st.write("Taxa de fraudes:", round(fraud_percentage, 2), "%")

    # Exibindo o dataframe
    st.subheader("Dados do Arquivo CSV")
    st.dataframe(df)


    # Filtrando por valores numéricos
    st.sidebar.subheader("Filtros")
    amount_range = st.sidebar.slider("Filtrar por valor da transação", float(df['Amount'].min()), float(df['Amount'].max()), (float(df['Amount'].min()), float(df['Amount'].max())))
    distance_range = st.sidebar.slider("Filtrar por distância para o estabelecimento", float(df['Distance to Merchant'].min()), float(df['Distance to Merchant'].max()), (float(df['Distance to Merchant'].min()), float(df['Distance to Merchant'].max())))

    # Filtrando por valores categóricos
    mcc_options = ['Todos'] + list(df['MCC'].unique())
    selected_mcc = st.sidebar.multiselect("Filtrar por código de categoria da transação (MCC)", mcc_options, default=['Todos'])

    fraud_options = ['Todos', 'Sim', 'Não']
    selected_fraud = st.sidebar.selectbox("Filtrar por transação fraudulenta", fraud_options)

    # Aplicando os filtros
    filtered_df = df.copy()
    if 'Todos' not in selected_mcc:
        filtered_df = filtered_df[filtered_df['MCC'].isin(selected_mcc)]
    if selected_fraud == 'Sim':
        filtered_df = filtered_df[filtered_df['Is Fraud'] == 1]
    elif selected_fraud == 'Não':
        filtered_df = filtered_df[filtered_df['Is Fraud'] == 0]
    filtered_df = filtered_df[
        (filtered_df['Amount'] >= amount_range[0]) &
        (filtered_df['Amount'] <= amount_range[1]) &
        (filtered_df['Distance to Merchant'] >= distance_range[0]) &
        (filtered_df['Distance to Merchant'] <= distance_range[1])
    ]

    # Exibindo informações do filtro
    st.subheader("Informações do Filtro")
    st.write("Quantidade de Transações Filtradas:", len(filtered_df))
    num_fraudulent_filtered_transactions = filtered_df['Is Fraud'].sum()
    st.write("Quantidade de Transações Fraudulentas Filtradas:", num_fraudulent_filtered_transactions)
    num_fraudulent_transactions_filtered = filtered_df['Is Fraud'].sum()
    fraud_percentage_filtered = (num_fraudulent_transactions_filtered / len(filtered_df)) * 100
    st.write("Taxa de fraudes no DataFrame filtrado:", round(fraud_percentage_filtered, 2), "%")


    # Exibindo o resultado filtrado
    st.subheader("Dados Filtrados")
    st.dataframe(filtered_df)

    # Gráfico de dia da semana com maior gasto de dinheiro
    df['Day of Week'] = filtered_df['Day of Week'].map({0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'})
    day_of_week_spending = df.groupby('Day of Week')['Amount'].sum()
    day_of_week_spending = day_of_week_spending.reindex(['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'])
    st.subheader("Dia da Semana com Maior Gasto de Dinheiro")
    fig, ax = plt.subplots()
    sns.barplot(x=day_of_week_spending.index, y=day_of_week_spending.values, ax=ax, order=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'])
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Total de Gasto de Dinheiro')
    ax.set_title('Gasto de Dinheiro por Dia da Semana')
    st.pyplot(fig)
    
    # Gráfico de transações fraudulentas por dia da semana
    filtered_df['Day of Week'] = filtered_df['Day of Week'].map({0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sáb', 6: 'Dom'})
    fraud_by_day_of_week = filtered_df.groupby('Day of Week')['Is Fraud'].sum()
    fraud_by_day_of_week = fraud_by_day_of_week.reindex(['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'])
    st.subheader("Transações Fraudulentas por Dia da Semana")
    fig, ax = plt.subplots()
    sns.lineplot(x=fraud_by_day_of_week.index, y=fraud_by_day_of_week.values, ax=ax)
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Total de Transações Fraudulentas')
    ax.set_title('Transações Fraudulentas por Dia da Semana')
    st.pyplot(fig)




    # Gráfico de valor total das transações por mês
    total_transactions_by_month = filtered_df.groupby('Month')['Amount'].sum()
    total_transactions_by_month = total_transactions_by_month.reindex(range(1, 13), fill_value=0)
    total_transactions_by_month.index = total_transactions_by_month.index.map(lambda x: calendar.month_abbr[x])
    st.subheader("Valor Total das Transações por Mês")
    fig, ax = plt.subplots()
    sns.barplot(x=total_transactions_by_month.index, y=total_transactions_by_month.values, ax=ax)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Valor Total das Transações')
    ax.set_title('Valor Total das Transações por Mês')
    st.pyplot(fig)

    # Filtrar transações fraudulentas
    fraudulent_transactions_by_month = filtered_df[filtered_df['Is Fraud'] == 1].groupby('Month').size()
    fraudulent_transactions_by_month = fraudulent_transactions_by_month.reindex(range(1, 13), fill_value=0)
    fraudulent_transactions_by_month.index = fraudulent_transactions_by_month.index.map(lambda x: calendar.month_abbr[x])

    # Plotar gráfico de quantidade de transações fraudulentas por mês
    st.subheader("Quantidade de Transações Fraudulentas por Mês")
    fig, ax = plt.subplots()
    sns.lineplot(x=fraudulent_transactions_by_month.index, y=fraudulent_transactions_by_month.values, ax=ax)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Quantidade de Transações Fraudulentas')
    ax.set_title('Quantidade de Transações Fraudulentas por Mês')
    st.pyplot(fig)
    
    # Gráfico de transações fraudulentas por horário
    fraud_by_hour = filtered_df.groupby('Hour')['Is Fraud'].sum()
    st.subheader("Transações Fraudulentas por Horário")
    fig, ax = plt.subplots()
    sns.lineplot(x=fraud_by_hour.index, y=fraud_by_hour.values, ax=ax)
    ax.set_xlabel('Horário')
    ax.set_ylabel('Total de Transações Fraudulentas')
    ax.set_title('Transações Fraudulentas por Horário')
    st.pyplot(fig)

    # Mapeando os códigos MCC para os nomes correspondentes
    # Carregar o arquivo JSON de mapeamento MCC
    with open('data/mcc.json', 'r') as file:
        mcc_mapping = json.load(file)

    # Criar um dicionário de mapeamento com base no arquivo JSON
    mcc_mapping_dict = {item['id']: item['description'] for item in mcc_mapping}

    # Converter os valores numéricos (id) para float
    mcc_mapping_dict = {int(key): value for key, value in mcc_mapping_dict.items()}

    # Gráfico de distribuição de fraudes por MCC
    fraud_by_mcc = filtered_df.groupby('MCC')['Is Fraud'].sum()
    fraud_by_mcc = fraud_by_mcc.sort_values(ascending=False).head(10)
    fraud_by_mcc.index = fraud_by_mcc.index.map(mcc_mapping_dict)

    try:
        st.subheader("Distribuição de Fraudes por MCC")
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.pie(fraud_by_mcc, labels=fraud_by_mcc.index, autopct='%1.1f%%')
        st.pyplot(fig)
    except ValueError:
        st.error("Não foi possível criar o gráfico de Distribuição de Fraudes por MCC devido aos resultados do filtro.")


if __name__ == '__main__':
    main()
