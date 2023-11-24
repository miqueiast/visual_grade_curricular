import streamlit as st
import pandas as pd

# Carregar dados da grade curricular a partir do arquivo Excel
file_path = 'grade_curricular.xlsx'  # Substitua pelo caminho real do seu arquivo
df = pd.read_excel(file_path)

# Seção sobre a história do Streamlit e exemplos
st.title('Explorando o Streamlit')

# História do Streamlit
st.markdown("""
    [Streamlit](https://streamlit.io/) é uma poderosa biblioteca de Python para criar aplicativos web interativos com facilidade.
    Ele foi projetado para simplificar o processo de transformar scripts de dados em aplicativos interativos sem exigir conhecimento avançado em desenvolvimento web.

    ### História do Streamlit

    O Streamlit foi lançado em 2019 por três engenheiros do Google - Adrien Treuille, Amanda Kelly e Thiago Teixeira.
    Sua visão era tornar a criação de aplicativos web tão simples quanto escrever scripts Python.
    Desde então, a comunidade do Streamlit cresceu rapidamente, e a biblioteca tornou-se uma escolha popular para cientistas de dados e desenvolvedores que desejam criar aplicativos interativos de maneira eficiente.
""")

# Exemplos de uso do Streamlit
st.title('Exemplos de Uso do Streamlit')

# Exemplo 1: Gráfico interativo
st.header('Gráfico Interativo')
st.markdown("""
    Vamos começar com um exemplo simples de um gráfico interativo usando o Streamlit.
    """)

# Código do exemplo 1
with st.echo():
    import matplotlib.pyplot as plt
    import numpy as np

    # Criar dados
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Plotar gráfico
    plt.plot(x, y)
    plt.title('Gráfico Interativo')
    st.pyplot()

st.markdown("""
    Este é apenas um exemplo básico, mas o Streamlit oferece suporte a uma variedade de elementos interativos,
    incluindo gráficos, widgets, botões e muito mais.
""")

# Seção sobre a Grade Curricular
st.title('Grade Curricular')

# Criar uma lista de períodos para a grade curricular
periodos = df['Período'].unique()

# Criar botões de seleção de período
selected_period = st.radio("Selecione o Período", periodos)

# Filtrar disciplinas do período selecionado
disciplinas_periodo = df[df['Período'] == selected_period]

# Mostrar informações na coluna correspondente
st.header(selected_period)
for index, row in disciplinas_periodo.iterrows():
    st.subheader(row['Nome'])
    st.markdown(f"Código: {row['Código']}")
    st.markdown(f"Carga Horária: {row['Carga Horária']} horas")
    st.markdown(f"Pré-requisito: {row['Pré-requisito']}")
    st.markdown(f"Ementa: {row['Ementa']}")
    st.markdown(f"Bibliografia: {row['Bibliografia']}")
