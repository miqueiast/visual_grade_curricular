import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Importando os dados
df_credit = pd.read_csv("german_credit_data.csv")

# Título do Dashboard
st.title("Análise de Risco de Crédito")

# Informações sobre os dados
st.write("Informações sobre os dados:")
st.write(df_credit.info())

# Visualização das primeiras linhas do conjunto de dados
st.write("Primeiras linhas do conjunto de dados:")
st.write(df_credit.head())

# Gráfico de barras para a variável alvo ("Risk")
fig1 = px.bar(df_credit, x=df_credit["Risk"].value_counts().index, y=df_credit["Risk"].value_counts().values,
              labels={'x': 'Variável de Risco', 'y': 'Contagem'}, title='Distribuição da variável alvo')

# Exibindo o gráfico de barras agrupado
st.plotly_chart(fig1)

# Análise da coluna "Credit amount" (Valor do Crédito) com gráficos de caixa
intervalo_idade = (18, 25, 35, 60, 120)
categorias_idade = ['Estudante', 'Jovem', 'Adulto', 'Idoso']
df_credit["Faixa Etária"] = pd.cut(df_credit.Age, intervalo_idade, labels=categorias_idade)

# Filtrando dados para "Bom Crédito" e "Crédito Ruim"
df_bom_credito = df_credit[df_credit["Risk"] == 'good']
df_credito_ruim = df_credit[df_credit["Risk"] == 'bad']

# Gráfico de caixa para relação entre idade, valor do crédito e categoria de idade
fig2 = px.box(df_bom_credito, x="Faixa Etária", y="Credit amount", color="Risk",
              labels={'x': 'Categoria de Idade', 'y': 'Valor do Crédito (Dólar Americano)'},
              title='Relação entre Idade, Valor do Crédito e Risco')

# Exibindo o gráfico de caixa
st.plotly_chart(fig2)

# Gráfico de barras para a variável "Housing" (Habitação)
fig3 = px.bar(df_credit, x=df_credit["Housing"].value_counts().index, y=df_credit["Housing"].value_counts().values,
              labels={'x': 'Tipo de Habitação', 'y': 'Contagem'}, title='Distribuição de Habitação')

# Exibindo o gráfico de barras
st.plotly_chart(fig3)

# Gráfico de violino para relação entre Habitação, Valor do Crédito e Risco
fig4 = px.violin(df_credit, x=df_credit["Housing"], y=df_credit["Credit amount"], color=df_credit["Risk"],
                 box=True, points="all", labels={'x': 'Tipo de Habitação', 'y': 'Valor do Crédito (Dólar Americano)'},
                 title='Relação entre Habitação, Valor do Crédito e Risco')

# Exibindo o gráfico de violino
st.plotly_chart(fig4)

# Gráficos de barras e caixas combinados para a variável "Saving accounts" (Contas de Poupança)
fig5 = px.histogram(df_credit, x="Saving accounts", color="Risk", marginal="box",
                    labels={'x': 'Contas de Poupança', 'y': 'Contagem'},
                    title='Exploração de Contas de Poupança')

# Exibindo o gráfico combinado
st.plotly_chart(fig5)

# Exibindo o DataFrame para referência
st.write("Visualização do DataFrame:")
st.write(df_credit)
