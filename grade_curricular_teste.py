import streamlit as st
import pandas as pd

# Carregamento dos dados
df = pd.read_excel('grade_curricular_1.xlsx')

# Mapear código de disciplina para o link correspondente
disciplina_links = {row['Código']: f"[{row['Nome']}](#{row['Código']})" for _, row in df.iterrows()}

# Agrupar por Período
periodos = df['Período'].unique()

# Criar uma seção para cada Período
for periodo in sorted(periodos):
    with st.expander(f"{periodo}"):
        # Filtrar o DataFrame para o período específico
        periodo_df = df[df['Período'] == periodo]

        # Exibir informações para cada disciplina no período
        for index, row in periodo_df.iterrows():
            checkbox_label = f"{row['Código']} - {row['Nome']} ({row['Carga Horária']} horas)"
            checkbox_state = st.checkbox(checkbox_label, key=f"checkbox_{index}")

            if checkbox_state:
                st.write(f"Ementa: {row['Ementa']}")
                st.write(f"Bibliografia: {row['Bibliografia']}")

                # Adicionar informações sobre os pré-requisitos, se existirem
                for i in range(1, 4):  # Assumindo que há até 3 colunas de pré-requisitos
                    col_name = f'Pré-requisito_{i}'
                    if not pd.isna(row[col_name]):
                        prereq_code = row[col_name]
                        prereq_link = disciplina_links.get(prereq_code, "Disciplina não encontrada")
                        st.write(f"Pré-requisito {i}: {prereq_link}")
