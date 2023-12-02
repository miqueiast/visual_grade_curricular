import streamlit as st
import pandas as pd
import io
import requests


# Função para carregar os dados
def carregar_dados(url):
    response = requests.get(url)
    return pd.read_excel(io.BytesIO(response.content), engine='openpyxl')


# Função para mapear código para nome
def mapear_codigo_para_nome(df):
    return dict(zip(df['Código'], df['Nome']))


# Função para adicionar informações de pré-requisitos
def adicionar_info_pre_requisitos(row, codigo_para_nome, codigo_para_periodo, cor_por_tipo):
    tipo_disciplina = row['Código'][:2]
    cor = cor_por_tipo.get(tipo_disciplina, 'DarkGrey')

    discipline_expander = st.expander(f'{row["Código"]} - {row["Nome"]}', expanded=False)

    with discipline_expander:
        st.write(f"Carga Horária: {row['Carga Horária']}")
        pre_requisitos_msg = obter_mensagem_requisitos(row['Pré-requisito'], codigo_para_nome, codigo_para_periodo)
        st.write(pre_requisitos_msg)
        requisitos_msg = obter_mensagem_requisitos(row['Requisito'], codigo_para_nome, codigo_para_periodo)
        st.write(requisitos_msg)
        st.write(f"Ementa: {row['Ementa']}")
        st.write(f"Bibliografia: {row['Bibliografia']}")


# Função para obter mensagem de pré-requisitos ou requisitos
def obter_mensagem_requisitos(requisitos, codigo_para_nome, codigo_para_periodo):
    requisitos_nomes = obter_nomes_e_periodos(requisitos, codigo_para_nome, codigo_para_periodo)
    return "Requisito: " + "\n".join(requisitos_nomes) if requisitos_nomes else "Requisito: Nenhum"


# Função para obter nomes e períodos a partir de códigos
def obter_nomes_e_periodos(codigos, codigo_para_nome, codigo_para_periodo):
    if pd.notna(codigos):
        codigos = str(codigos)  # Certificar-se de que é uma string
        if '/' in codigos:
            return [
                f"{codigo} - {codigo_para_nome.get(codigo, '')} ({codigo_para_periodo.get(codigo, '')})"
                for codigo in codigos.split('/') if codigo
            ]
        else:
            return [f"{codigos} - {codigo_para_nome.get(codigos, '')} ({codigo_para_periodo.get(codigos, '')})"]
    else:
        return []


# Carregamento dos dados do link
url = 'https://github.com/miqueiast/visual_grade_curricular/raw/main/grade_curricular.xlsx'
df = carregar_dados(url)

# Mapear Código para Nome para facilitar a busca de pré-requisitos
codigo_para_nome = mapear_codigo_para_nome(df)
codigo_para_periodo = dict(zip(df['Código'], df['Período']))

# Adicionar coluna 'Requisito' ao DataFrame
df['Requisito'] = ''

# Preencher a coluna 'Requisito' com base nas informações de pré-requisito
df['Requisito'] = df['Código'].apply(
    lambda x: '/'.join(df[df['Pré-requisito'].str.contains(x, na=False)]['Código'].tolist()))

# Agrupar por Período
periodos = df['Período'].unique()

# Configurar o layout da página
st.set_page_config(layout="wide", page_icon=None, page_title=None, initial_sidebar_state="auto")

# Criar duas colunas para posicionar as imagens lado a lado
col1, col2 = st.columns(2)

# Adicionar a primeira imagem na primeira coluna
col1.image("estatisticacienciadedados.png", width=720)  # Substitua pelo caminho da sua primeira imagem e ajuste a largura conforme necessário

# Adicionar espaçamento entre as colunas usando st.markdown
col1.markdown("&nbsp;", unsafe_allow_html=True)

# Adicionar um título
st.title("Visualização da Grade Curricular")

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
cores_por_periodo = {'1': 'LightBlue', '2': 'LightGreen', '3': 'LightSalmon', '4': 'LightPink',
                     '5': 'LightGoldenRodYellow'}

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
                adicionar_info_pre_requisitos(row, codigo_para_nome, codigo_para_periodo, cor_por_tipo)