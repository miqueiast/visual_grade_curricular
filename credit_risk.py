import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Importando os dados
df_credit = pd.read_csv("german_credit_data.csv")

# Título do Dashboard
st.title("Análise de Risco de Crédito")

# Caixas de seleção para filtrar por Age
selected_age_values = st.multiselect("Selecione os valores para Age", df_credit["Age"].unique())

# Caixas de seleção para filtrar por Sex
selected_sex_values = st.multiselect("Selecione os valores para Sex", df_credit["Sex"].unique())

# Filtrando o DataFrame com base nas seleções
df_filtered = df_credit[df_credit["Age"].isin(selected_age_values) & df_credit["Sex"].isin(selected_sex_values)]

# Resetando o índice para evitar o erro de coluna duplicada
df_filtered.reset_index(drop=True, inplace=True)

# Exibindo os dados filtrados
st.write("Dados filtrados:")
st.table(df_filtered)

# Informações sobre os dados
st.write("Informações sobre os dados:")
st.write(df_credit.info())

# Gráfico de barras para a variável alvo ("Risk") usando dados filtrados
fig1 = px.bar(df_filtered, x=df_filtered["Risk"].value_counts().index, y=df_filtered["Risk"].value_counts().values,
              labels={'x': 'Variável de Risco', 'y': 'Contagem'}, title='Distribuição da variável alvo')

# Exibindo o gráfico de barras agrupado
st.plotly_chart(fig1)

# Análise da coluna "Credit amount" (Valor do Crédito) com gráficos de caixa
intervalo_idade = (18, 25, 35, 60, 120)
categorias_idade = ['Estudante', 'Jovem', 'Adulto', 'Idoso']
df_filtered["Faixa Etária"] = pd.cut(df_filtered.Age, intervalo_idade, labels=categorias_idade)

# Filtrando dados para "Bom Crédito" e "Crédito Ruim"
df_bom_credito = df_filtered[df_filtered["Risk"] == 'Crédito Saudável']
df_credito_ruim = df_filtered[df_filtered["Risk"] == 'Crédito Ruim']

# Gráfico de caixa para relação entre idade, valor do crédito e categoria de idade
fig2 = px.box(df_bom_credito, x="Faixa Etária", y="Credit amount", color="Risk",
              labels={'x': 'Categoria de Idade', 'y': 'Valor do Crédito (Dólar Americano)'},
              title='Relação entre Idade, Valor do Crédito e Risco')

# Exibindo o gráfico de caixa
st.plotly_chart(fig2)

# Gráfico de barras para a variável "Housing" (Habitação) usando dados filtrados
fig3 = px.bar(df_filtered, x=df_filtered["Housing"].value_counts().index, y=df_filtered["Housing"].value_counts().values,
              labels={'x': 'Tipo de Habitação', 'y': 'Contagem'}, title='Distribuição de Habitação')

# Exibindo o gráfico de barras
st.plotly_chart(fig3)

# Gráfico de violino para relação entre Habitação, Valor do Crédito e Risco
fig4 = px.violin(df_filtered, x=df_filtered["Housing"], y=df_filtered["Credit amount"], color=df_filtered["Risk"],
                 box=True, points="all", labels={'x': 'Tipo de Habitação', 'y': 'Valor do Crédito (Dólar Americano)'},
                 title='Relação entre Habitação, Valor do Crédito e Risco')

# Exibindo o gráfico de violino
st.plotly_chart(fig4)