import streamlit as st
import pandas as pd

# Carregar dados da grade curricular a partir do arquivo Excel
file_path = 'grade_curricular.xlsx'  # Substitua pelo caminho real do seu arquivo
df = pd.read_excel(file_path)

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
