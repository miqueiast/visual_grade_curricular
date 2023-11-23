import streamlit as st
import pandas as pd

# Dados fictícios para a grade curricular
dados_grade_curricular = {
    'Disciplina': ['Matemática', 'Física', 'Programação', 'Banco de Dados'],
    'Ementa': ['Ementa de Matemática', 'Ementa de Física', 'Ementa de Programação', 'Ementa de Banco de Dados'],
    'Pré-requisitos': ['', 'Matemática', 'Matemática', '']
}

df = pd.DataFrame(dados_grade_curricular)

# Criar uma tabela interativa com Streamlit

# Seção de seleção de disciplina
st.title('Grade Curricular')
disciplina_selecionada = st.selectbox('Selecione uma disciplina:', df['Disciplina'])

# Seção de detalhes da disciplina
if disciplina_selecionada:
    st.subheader('Detalhes da Disciplina')
    st.write(f"**Nome da Disciplina:** {disciplina_selecionada}")
    st.write(f"**Ementa:** {df[df['Disciplina'] == disciplina_selecionada]['Ementa'].values[0]}")
    st.write(f"**Pré-requisitos:** {df[df['Disciplina'] == disciplina_selecionada]['Pré-requisitos'].values[0]}")
else:
    st.warning("Selecione uma disciplina para ver os detalhes.")

# Seção da tabela completa
st.subheader('Tabela Completa')
st.write(df)