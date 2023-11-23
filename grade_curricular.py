import streamlit as st
import pandas as pd

# Dados fictícios para a grade curricular
dados_grade_curricular = {
    'Período': ['1º Período', '2º Período', '3º Período'],
    'Disciplina': ['Matemática', 'Física', 'Programação'],
    'Ementa': ['Ementa de Matemática', 'Ementa de Física', 'Ementa de Programação'],
    'Pré-requisitos': ['', 'Matemática', 'Matemática']
}

df = pd.DataFrame(dados_grade_curricular)

# Criar uma grade curricular

# Criar uma lista de disciplinas para cada período
periodos = df['Período'].unique()

# Criar colunas para cada período
num_colunas = len(periodos)
colunas = st.columns(num_colunas)

for i, periodo in enumerate(periodos):
    disciplinas = df[df['Período'] == periodo]['Disciplina'].tolist()

    # Mostrar informações na coluna correspondente
    with colunas[i]:
        st.header(periodo)
        for disciplina in disciplinas:
            st.subheader(disciplina)
            st.text(f"Ementa: {df[df['Disciplina'] == disciplina]['Ementa'].values[0]}")
            st.text(f"Pré-requisitos: {df[df['Disciplina'] == disciplina]['Pré-requisitos'].values[0]}")
