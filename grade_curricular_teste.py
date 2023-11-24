import streamlit as st
import pandas as pd

# Carregamento dos dados
df = pd.read_excel('grade_curricular.xlsx')

# Agrupar por Período
periodos = df['Período'].unique()

# Criar uma seção para cada Período
for periodo in sorted(periodos):
    with st.expander(f"{periodo}"):
        # Filtrar o DataFrame para o período específico
        periodo_df = df[df['Período'] == periodo]
        
        # Exibir informações para cada disciplina no período
        for index, row in periodo_df.iterrows():
            st.write(f"{row['Código']} - {row['Nome']} ({row['Carga Horária']} horas)")

# Criar uma seção para as Optativas
optativas_df = df[df['Período'] == 'Optativas']
