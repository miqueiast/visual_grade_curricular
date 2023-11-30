import streamlit as st
import pandas as pd
import io
import requests

# Carregamento dos dados do link
url = 'https://github.com/miqueiast/visual_grade_curricular/raw/main/grade_curricular.xlsx'
response = requests.get(url)
df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')

# Mapear Código para Nome para facilitar a busca de pré-requisitos
codigo_para_nome = dict(zip(df['Código'], df['Nome']))
codigo_para_periodo = dict(zip(df['Código'], df['Período']))

# Adicionar coluna 'Requisito' ao DataFrame
df['Requisito'] = ''

# Preencher a coluna 'Requisito' com base nas informações de pré-requisito
for index, row in df.iterrows():
    disciplina_codigo = row['Código']
    requisitos_para_disciplina = df[df['Pré-requisito'].str.contains(disciplina_codigo, na=False)]
    requisitos_codigos = requisitos_para_disciplina['Código'].tolist()
    df.at[index, 'Requisito'] = '/'.join(requisitos_codigos)

# Agrupar por Período
periodos = df['Período'].unique()

# Configurar o layout da página
st.set_page_config(layout="wide")

# Adicionar um título
st.title("Visualização de Grade Curricular")

# Criar um contêiner para os períodos
container = st.container()

# Definir cores para os tipos de disciplinas
cor_por_tipo = {'CE': 'DodgerBlue', 'CI': 'DarkGreen', 'CM': 'DarkOrange'}

# Script JavaScript para ajustar dinamicamente a altura do botão do Período
script = """
<script>
  const buttons = document.querySelectorAll('.period-button');
  buttons.forEach(button => {
    const expander = button.nextElementSibling.querySelector('.stExpander')
    button.style.height = expander.scrollHeight + 'px';
  });
</script>
"""

# Adicionar o script JavaScript ao Streamlit
st.markdown(script, unsafe_allow_html=True)

# Defina uma paleta de cores para os períodos
cores_por_periodo = {'1': 'LightBlue', '2': 'LightGreen', '3': 'LightSalmon', '4': 'LightPink', '5': 'LightGoldenRodYellow'}

# Criar uma seção para cada Período
for periodo in sorted(periodos):
    with container:
        # Criar uma coluna para o botão do Período
        col1, col2 = st.columns([1, 10])
        with col1:
            # Calcular a altura dinamicamente baseada na quantidade de disciplinas
            altura_botao = 10 + len(df[df['Período'] == periodo]) * 60  # Ajuste conforme necessário
            # Definir width e margin-top para o botão do Período
            cor_background = cores_por_periodo.get(str(periodo), 'LightGrey')
            st.markdown(
                f'<button class="period-button" style="height: {altura_botao}px; width: 100px; margin-top: 5px; background-color: {cor_background};">{periodo}</button>',
                unsafe_allow_html=True
            )
        
        # Criar uma coluna para as disciplinas
        with col2:
            # Filtrar o DataFrame para o período específico
            periodo_df = df[df['Período'] == periodo]
            
            # Exibir as disciplinas do período
            for i, (index, row) in enumerate(periodo_df.iterrows()):
                tipo_disciplina = row['Código'][:2]
                cor = cor_por_tipo.get(tipo_disciplina, 'DarkGrey')

                # Definir um espaçamento adicional para a primeira disciplina
                margin_top = '50px' if i == 0 else '5px'

                # Estilizar a disciplina com base na cor
                discipline_expander = st.expander(f'{row["Código"]} - {row["Nome"]}', expanded=False)
                
                with discipline_expander:
                    st.write(f"Carga Horária: {row['Carga Horária']}")
                    
                    # Adicionar informações de pré-requisitos
                    pre_requisitos = row['Pré-requisito']
                    if pd.notna(pre_requisitos):
                        pre_requisitos_nomes = [
                            f"{codigo} - {codigo_para_nome.get(codigo, '')} ({codigo_para_periodo.get(codigo, '')})"
                            for codigo in pre_requisitos.split('/')
                        ]
                        pre_requisitos_nomes = [nome for nome in pre_requisitos_nomes if nome]  # Remover valores nulos
                        if pre_requisitos_nomes:
                            st.write("Pré-requisito:")
                            for nome in pre_requisitos_nomes:
                                st.write(nome)
                        else:
                            st.write("Pré-requisito: Nenhum")
                    else:
                        st.write("Pré-requisito: Nenhum")

                    # Adicionar informações de pré-requisitos
                    requisitos = row['Requisito']
                    if pd.notna(requisitos) and requisitos != "":
                        requisitos_nomes = [
                            f"{codigo} - {codigo_para_nome.get(codigo, '')} ({codigo_para_periodo.get(codigo, '')})"
                            for codigo in requisitos.split('/')
                        ]
                        requisitos_nomes = [nome for nome in requisitos_nomes if nome]  # Remove null values
                        if requisitos_nomes:
                            st.write("Requisito:")
                            for nome in requisitos_nomes:
                                st.write(nome)
                        else:
                            st.write("Requisito: Nenhum")
                    else:
                        st.write("Requisito: Nenhum")



                                
                    st.write(f"Ementa: {row['Ementa']}")
                    st.write(f"Bibliografia: {row['Bibliografia']}")
