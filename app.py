import streamlit as st
import pandas as pd
import json
import plotly.express as px

@st.cache
def carregar_dados():
    with open('transacoesLIGHT.json', 'r', encoding='utf-8') as file:
        dados = json.load(file)
        df = pd.json_normalize(dados)
        df['data_hora'] = pd.to_datetime(df['data_hora'])
        return df

dados = carregar_dados()

# Barra lateral para seleção de cliente
clientes = dados['cliente.nome'].unique()
cliente_selecionado = st.sidebar.selectbox('Selecione o cliente', clientes)

# Filtra dados pelo cliente selecionado
dados_cliente = dados[dados['cliente.nome'] == cliente_selecionado]

# Exibe gráfico de gastos por categoria do cliente selecionado
fig1 = px.pie(dados_cliente, values='valor', names='estabelecimento.categoria', title='Gastos por Categoria')
st.plotly_chart(fig1)

# Exibe gráfico de gastos por mês do cliente selecionado
dados_cliente['mes'] = dados_cliente['data_hora'].dt.month_name()
gastos_por_mes = dados_cliente.groupby('mes')['valor'].sum()
fig2 = px.bar(gastos_por_mes, x=gastos_por_mes.index, y='valor', title='Gastos por Mês')
st.plotly_chart(fig2)

# Exibe média e mediana de gastos do cliente selecionado
media_gastos = dados_cliente['valor'].mean()
mediana_gastos = dados_cliente['valor'].median()
st.write(f'Média de gastos: R${media_gastos:.2f}')
st.write(f'Mediana de gastos: R${mediana_gastos:.2f}')

# Exibe tabela com todas as transações do cliente selecionado
st.subheader(f'Todas as transações de {cliente_selecionado}')
st.write(dados_cliente)
