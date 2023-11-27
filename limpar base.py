import pandas as pd

# Carregamento dos dados
df = pd.read_excel('grade_curricular.xlsx')

# Suponha que a coluna 'Pré-requisitos' contenha os códigos de pré-requisitos separados por '/'
df['Pré-requisito'] = df['Pré-requisito'].str.split('/')

# Expande a lista de códigos de pré-requisitos em colunas separadas
df = df.explode('Pré-requisito').reset_index(drop=True)

# Salva o DataFrame de volta no arquivo Excel, se necessário
df.to_excel('grade_curricular_nova.xlsx', index=False)
