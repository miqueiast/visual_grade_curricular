import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carregando os dados
url = "https://raw.githubusercontent.com/miqueiast/visual_grade_curricular/main/german_credit_data.csv"
df_credit = pd.read_csv(url, index_col=0)


# Configurando a página do Streamlit
st.set_page_config(page_title='Análise de Crédito Alemã', layout='wide')

# Título do aplicativo
st.title('Análise de Dados de Crédito Alemães')

# Filtro deslizante para a idade
idade_intervalo = st.sidebar.slider('Selecione Faixa Etária', int(df_credit['Age'].min()), int(df_credit['Age'].max()), (int(df_credit['Age'].min()), int(df_credit['Age'].max())))

# Filtro para o sexo
opcoes_sexuais = ['Ambos'] + df_credit['Sex'].unique().tolist()
sexo_selecionado = st.sidebar.selectbox('Selecione o Sexo', opcoes_sexuais, index=0)

# Filtrar o dataframe com base nos filtros selecionados
df_filtrado = df_credit[(df_credit['Age'] >= idade_intervalo[0]) & (df_credit['Age'] <= idade_intervalo[1])]

if sexo_selecionado != 'Ambos':
    df_filtrado = df_filtrado[df_filtrado['Sex'] == sexo_selecionado]

# Algumas visualizações e explorações
st.header('Análise da Distribuição Etária')

# Histograma de Distribuição de Idade
fig_distribuicao_idade = px.histogram(df_filtrado, x='Age', histnorm='probability', title=f'Distribuição Etária para Faixa Etária: {idade_intervalo[0]}-{idade_intervalo[1]}')
fig_distribuicao_idade.update_layout(bargap=0.05)
st.plotly_chart(fig_distribuicao_idade)

# Visualização de contagens de algumas variáveis categóricas
st.header('Contagem de Características Categóricas')

fig_contagens, axes_contagens = plt.subplots(2, 2, figsize=(12, 10))

sns.countplot(x='Sex', data=df_filtrado, hue='Risk', palette='Set1', ax=axes_contagens[0, 0])
sns.countplot(x='Housing', data=df_filtrado, hue='Risk', palette='Set2', ax=axes_contagens[0, 1])
sns.countplot(x='Job', data=df_filtrado, hue='Risk', palette='Set3', ax=axes_contagens[1, 0])
sns.countplot(x='Saving accounts', data=df_filtrado, hue='Risk', palette='Set1', ax=axes_contagens[1, 1])

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
    x=df_filtrado['Housing'],
    y=df_filtrado['Credit amount'],
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
    x=df_filtrado['Job'],
    y=df_filtrado['Credit amount'],
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
    x=df_filtrado['Saving accounts'],
    y=df_filtrado['Credit amount'],
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
    x=df_filtrado[df_filtrado["Risk"] == 'good']["Sex"].value_counts().index.values,
    y=df_filtrado[df_filtrado["Risk"] == 'good']["Sex"].value_counts().values,
    name='Bom crédito'
)

trace1 = go.Bar(
    x=df_filtrado[df_filtrado["Risk"] == 'bad']["Sex"].value_counts().index.values,
    y=df_filtrado[df_filtrado["Risk"] == 'bad']["Sex"].value_counts().values,
    name="Mau Crédito"
)

# Boxplot
trace2 = go.Box(
    x=df_filtrado[df_filtrado["Risk"] == 'good']["Sex"],
    y=df_filtrado[df_filtrado["Risk"] == 'good']["Credit amount"],
    name=trace0.name,
    marker=dict(color='lightblue')  # Defina a cor desejada para 'good'
)

trace3 = go.Box(
    x=df_filtrado[df_filtrado["Risk"] == 'bad']["Sex"],
    y=df_filtrado[df_filtrado["Risk"] == 'bad']["Credit amount"],
    name=trace1.name,
    marker=dict(color='salmon')  # Defina a cor desejada para 'bad'
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