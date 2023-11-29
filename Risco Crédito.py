import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carregando os dados
url = "https://github.com/miqueiast/visual_grade_curricular/raw/main/dados_transformados.csv"

# Tentar ler o arquivo CSV com tratamento de exceção
try:
    df_credit = pd.read_csv(url, index_col=0)
except pd.errors.ParserError as e:
    st.error(f"Erro ao ler o arquivo CSV: {e}")
    st.stop()

# Configurando a página do Streamlit
st.set_page_config(page_title='Análise de Crédito Alemã', layout='wide')

# Título do aplicativo
st.title('Análise de Dados de Crédito Alemães')

# Filtro deslizante para a idade
idade_intervalo = st.sidebar.slider('Selecione Faixa Etária', int(df_credit['Idade'].min()), int(df_credit['Idade'].max()), (int(df_credit['Idade'].min()), int(df_credit['Idade'].max())))

# Filtro para o sexo
opcoes_sexuais = ['Ambos'] + df_credit['Sexo'].unique().tolist()
sexo_selecionado = st.sidebar.selectbox('Selecione o Sexo', opcoes_sexuais, index=0)

# Filtro para a profissão
opcoes_profissao = ['Todas'] + df_credit['Profissao'].unique().tolist()
profissao_selecionada = st.sidebar.selectbox('Selecione a Profissão', opcoes_profissao, index=0)

# Filtrar o dataframe com base nos filtros selecionados
df_filtrado = df_credit[(df_credit['Idade'] >= idade_intervalo[0]) & (df_credit['Idade'] <= idade_intervalo[1])]

if sexo_selecionado != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['Sexo'] == sexo_selecionado]

# Filtrar o dataframe com base na profissão selecionada
if profissao_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Profissao'] == profissao_selecionada]

# Algumas visualizações e explorações
st.header('Análise da Distribuição Etária')

# Histograma de Distribuição de Idade
fig_distribuicao_idade = px.histogram(df_filtrado, x='Idade', histnorm='probability', title=f'Distribuição Etária para Faixa Etária: {idade_intervalo[0]}-{idade_intervalo[1]}')
fig_distribuicao_idade.update_layout(bargap=0.05)
st.plotly_chart(fig_distribuicao_idade)

# Visualização de contagens de algumas variáveis categóricas
st.header('Contagem de Características Categóricas')

fig_contagens, axes_contagens = plt.subplots(2, 2, figsize=(12, 10))

sns.countplot(x='Sexo', data=df_filtrado, hue='Risco', palette='Set1', ax=axes_contagens[0, 0])
sns.countplot(x='Moradia', data=df_filtrado, hue='Risco', palette='Set2', ax=axes_contagens[0, 1])
sns.countplot(x='Profissao', data=df_filtrado, hue='Risco', palette='Set3', ax=axes_contagens[1, 0])
sns.countplot(x='Conta_Poupanca', data=df_filtrado, hue='Risco', palette='Set1', ax=axes_contagens[1, 1])

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.suptitle('Contagem de Características Categóricas', fontsize=16)
st.pyplot(fig_contagens)

# Visualização de correlações
st.header('Matriz de Correlação')

colunas_numericas = df_filtrado.select_dtypes(include=[np.number]).columns
df_numeric = df_filtrado[colunas_numericas]

fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', linewidths=.5, ax=ax_corr)
plt.title('Matriz de Correlação', fontsize=16)
st.pyplot(fig_corr)

# Adicionando o gráfico de violino para Housing
st.header('Tipo de Moradia vs. Valor do Crédito (Violin Plot)')

fig_violino_moradia = go.Figure()

fig_violino_moradia.add_trace(go.Violin(
    x=df_filtrado['Moradia'],
    y=df_filtrado['Valor_do_Credito'],
    legendgroup='Moradia',
    scalegroup='No',
    name='Moradia',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='orange'
))

fig_violino_moradia.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violino_moradia)

# Adicionando o gráfico de violino para Job
st.header('Profissão vs. Valor do Crédito (Violin Plot)')

fig_violino_profissao = go.Figure()

fig_violino_profissao.add_trace(go.Violin(
    x=df_filtrado['Profissao'],
    y=df_filtrado['Valor_do_Credito'],
    legendgroup='Profissao',
    scalegroup='No',
    name='Profissao',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='purple'
))

fig_violino_profissao.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violino_profissao)

# Adicionando o gráfico de violino para Saving accounts
st.header('Conta Poupança vs. Valor do Crédito (Violin Plot)')

fig_violino_conta_poupanca = go.Figure()

fig_violino_conta_poupanca.add_trace(go.Violin(
    x=df_filtrado['Conta_Poupanca'],
    y=df_filtrado['Valor_do_Credito'],
    legendgroup='Conta Poupanca',
    scalegroup='No',
    name='Conta Poupanca',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='green'
))

fig_violino_conta_poupanca.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violino_conta_poupanca)

# Gráfico de barras e boxplot para Sexo
st.header('Análise da Distribuição por Sexo')

# Gráfico de barras
trace0 = go.Bar(
    x=df_filtrado[df_filtrado["Risco"] == "Crédito Bom"]["Sexo"].value_counts().index.values,
    y=df_filtrado[df_filtrado["Risco"] == "Crédito Bom"]["Sexo"].value_counts().values,
    name='Crédito Bom'
)

trace1 = go.Bar(
    x=df_filtrado[df_filtrado["Risco"] == "Crédito Ruim"]["Sexo"].value_counts().index.values,
    y=df_filtrado[df_filtrado["Risco"] == "Crédito Ruim"]["Sexo"].value_counts().values,
    name="Crédito Ruim"
)

# Boxplot
trace2 = go.Box(
    x=df_filtrado[df_filtrado["Risco"] == "Crédito Bom"]["Sexo"],
    y=df_filtrado[df_filtrado["Risco"] == "Crédito Bom"]["Valor_do_Credito"],
    name=trace0.name,
    marker=dict(color='lightblue')  # Defina a cor desejada para "Crédito Bom"
)

trace3 = go.Box(
    x=df_filtrado[df_filtrado["Risco"] == "Crédito Ruim"]["Sexo"],
    y=df_filtrado[df_filtrado["Risco"] == "Crédito Ruim"]["Valor_do_Credito"],
    name=trace1.name,
    marker=dict(color='salmon')  # Defina a cor desejada para "Crédito Ruim"
)

dados_distribuicao_sexo = [trace0, trace1, trace2, trace3]

fig_distribuicao_sexo = make_subplots(rows=1, cols=2,
                                      subplot_titles=('Contagem de Sexo', 'Valor do Crédito por Sexo'))

fig_distribuicao_sexo.add_trace(trace0, 1, 1)
fig_distribuicao_sexo.add_trace(trace1, 1, 1)
fig_distribuicao_sexo.add_trace(trace2, 1, 2)
fig_distribuicao_sexo.add_trace(trace3, 1, 2)

fig_distribuicao_sexo.update_layout(height=400, width=800, title='Distribuição por Sexo', boxmode='group')

st.plotly_chart(fig_distribuicao_sexo)