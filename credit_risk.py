# Importing libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Added import statement

# Carregando os dados
df_credit = pd.read_csv("german_credit_data.csv", index_col=0)

# Configurando a página do Streamlit
st.set_page_config(page_title='German Credit Analysis', layout='wide')

# Título do aplicativo
st.title('German Credit Data Analysis')

# Filtro deslizante para a idade
age_range = st.slider('Select Age Range', int(df_credit['Age'].min()), int(df_credit['Age'].max()), (int(df_credit['Age'].min()), int(df_credit['Age'].max())))

# Algumas visualizações e explorações
st.header('Age Distribution Analysis')

df_good = df_credit[df_credit["Risk"] == 'good']
df_bad = df_credit[df_credit["Risk"] == 'bad']

filtered_df = df_credit[(df_credit['Age'] >= age_range[0]) & (df_credit['Age'] <= age_range[1])]

fig_age_distribution = px.histogram(filtered_df, x='Age', histnorm='probability', title=f'Age Distribution for Age Range: {age_range[0]}-{age_range[1]}')
fig_age_distribution.update_layout(bargap=0.05)
st.plotly_chart(fig_age_distribution)

# Visualização de contagens de algumas variáveis categóricas
st.header('Categorical Features Count')

fig_counts, axes_counts = plt.subplots(2, 2, figsize=(12, 10))

sns.countplot(x='Sex', data=filtered_df, hue='Risk', palette='Set1', ax=axes_counts[0, 0])
sns.countplot(x='Housing', data=filtered_df, hue='Risk', palette='Set2', ax=axes_counts[0, 1])
sns.countplot(x='Job', data=filtered_df, hue='Risk', palette='Set3', ax=axes_counts[1, 0])
sns.countplot(x='Saving accounts', data=filtered_df, hue='Risk', palette='Set1', ax=axes_counts[1, 1])

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.suptitle('Categorical Features Count', fontsize=16)
st.pyplot(fig_counts)

# Visualização de correlações
st.header('Correlation Matrix')

numeric_columns = filtered_df.select_dtypes(include=[np.number]).columns
df_numeric = filtered_df[numeric_columns]

fig_corr, ax_corr = plt.subplots(figsize=(12, 10))
sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', linewidths=.5, ax=ax_corr)
plt.title('Correlation Matrix', fontsize=16)
st.pyplot(fig_corr)

# Adicionando o gráfico de violino
st.header('Housing vs. Credit Amount (Violin Plot)')

fig_violin_housing = go.Figure()

fig_violin_housing.add_trace(go.Violin(
    x=filtered_df['Housing'],
    y=filtered_df['Credit amount'],
    legendgroup='Housing',
    scalegroup='No',
    name='Housing',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='orange'
))

fig_violin_housing.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violin_housing)

# Adicionando o gráfico de violino para Job
st.header('Job vs. Credit Amount (Violin Plot)')

fig_violin_job = go.Figure()

fig_violin_job.add_trace(go.Violin(
    x=filtered_df['Job'],
    y=filtered_df['Credit amount'],
    legendgroup='Job',
    scalegroup='No',
    name='Job',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='purple'
))

fig_violin_job.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violin_job)

# Adicionando o gráfico de violino para Saving accounts
st.header('Saving Accounts vs. Credit Amount (Violin Plot)')

fig_violin_saving_accounts = go.Figure()

fig_violin_saving_accounts.add_trace(go.Violin(
    x=filtered_df['Saving accounts'],
    y=filtered_df['Credit amount'],
    legendgroup='Saving Accounts',
    scalegroup='No',
    name='Saving Accounts',
    side='positive',
    box_visible=True,
    meanline_visible=True,
    line_color='green'
))

fig_violin_saving_accounts.update_layout(
    yaxis=dict(zeroline=False),
    violingap=0,
    violinmode='overlay'
)

st.plotly_chart(fig_violin_saving_accounts)

# First plot
trace0 = go.Bar(
    x=filtered_df[filtered_df["Risk"] == 'good']["Sex"].value_counts().index.values,
    y=filtered_df[filtered_df["Risk"] == 'good']["Sex"].value_counts().values,
    name='Good credit'
)

# First plot 2
trace1 = go.Bar(
    x=filtered_df[filtered_df["Risk"] == 'bad']["Sex"].value_counts().index.values,
    y=filtered_df[filtered_df["Risk"] == 'bad']["Sex"].value_counts().values,
    name="Bad Credit"
)

# Second plot
trace2 = go.Box(
    x=filtered_df[filtered_df["Risk"] == 'good']["Sex"],
    y=filtered_df[filtered_df["Risk"] == 'good']["Credit amount"],
    name=trace0.name
)

# Second plot 2
trace3 = go.Box(
    x=filtered_df[filtered_df["Risk"] == 'bad']["Sex"],
    y=filtered_df[filtered_df["Risk"] == 'bad']["Credit amount"],
    name=trace1.name
)

data = [trace0, trace1, trace2, trace3]

fig_sex_distribution = make_subplots(rows=1, cols=2,
                                     subplot_titles=('Sex Count', 'Credit Amount by Sex'))

fig_sex_distribution.add_trace(trace0, 1, 1)
fig_sex_distribution.add_trace(trace1, 1, 1)
fig_sex_distribution.add_trace(trace2, 1, 2)
fig_sex_distribution.add_trace(trace3, 1, 2)

fig_sex_distribution.update_layout(height=400, width=800, title='Sex Distribution', boxmode='group')

st.plotly_chart(fig_sex_distribution)
