import pandas as pd
import numpy as np
import datetime
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()


# # --- 1. Lendo o arquivo JSONL e configurando o DataFrame ---
pd.options.display.max_columns = None
JSON_FOLDER_PATH = os.environ.get("JSON_FOLDER_PATH")
notebook_data = pd.read_json(JSON_FOLDER_PATH, lines=True)

#Adicionar a hora da extração/transformação
notebook_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Tratar Nulos
notebook_data['old_price'] = notebook_data['old_price'].fillna(0)
notebook_data['new_price'] = notebook_data['new_price'].fillna(0)
notebook_data['reviews_rating'] = notebook_data['reviews_rating'].fillna(0)
notebook_data['reviews_count'] = notebook_data['reviews_count'].fillna(0)

#Tratamentos dos dados
notebook_data['old_price'] = notebook_data['old_price'].astype(str).str.replace('.', '', regex=False)
notebook_data['new_price'] = notebook_data['new_price'].astype(str).str.replace('.', '', regex=False)
notebook_data['reviews_count'] = notebook_data['reviews_count'].astype(str).str.replace('[\(\)]', '', regex=True)

#Converter os tipos de dados.
notebook_data['old_price'] = notebook_data['old_price'].astype(float)
notebook_data['new_price'] = notebook_data['new_price'].astype(float)
notebook_data['reviews_count'] = notebook_data['reviews_count'].astype(int)
notebook_data['reviews_rating'] = notebook_data['reviews_rating'].astype(float)

#Criando cálculos adicionais
notebook_data['discount'] = np.where( notebook_data['new_price'] != 0, (notebook_data['old_price'] - notebook_data['new_price']), 0)

# Criando a coluna de categoria de avaliação
# 1. Definir as Condições (a ordem importa!)
# Começamos tratando nulos/zeros, depois vamos das notas mais altas para as mais baixas.
conditions = [
    notebook_data['reviews_rating'].isnull(),
    notebook_data['reviews_rating'] == 0,  # Trata o 0 explicitamente
    notebook_data['reviews_rating'] >= 4.5,
    notebook_data['reviews_rating'] >= 4.0, # Captura de 4.0 a 4.49...
    notebook_data['reviews_rating'] >= 3.0, # Captura de 3.0 a 3.99...
    notebook_data['reviews_rating'] > 0      # Captura qualquer valor > 0 e < 3.0
]

# 2. Definir os Resultados correspondentes a cada condição
choices = [
    'Sem Avaliação',  # Resultado para isnull()
    'Sem Avaliação',  # Resultado para == 0 (ou pode ser 'Avaliação Zero')
    'Excelente',      # Resultado para >= 4.5
    'Bom',            # Resultado para >= 4.0
    'Regular',        # Resultado para >= 3.0
    'Ruim'            # Resultado para > 0 (e < 3.0)
]

# 3. Criar a nova coluna usando np.select
# O argumento 'default' é usado se NENHUMA condição for atendida
notebook_data['rating_category'] = np.select(conditions, choices, default='Indefinido')

# Criando a coluna de categoria de contagem de avaliações, pois a quantidade de reviews é um componente importante quando olhando para a review rating.
# 1. Definir as Condições (a ordem importa!)
conditions = [
    notebook_data['reviews_count'] <= 0,
    notebook_data['reviews_count'] < 10,
    notebook_data['reviews_count'] < 100,
    notebook_data['reviews_count'] < 1000,
    notebook_data['reviews_count'] >= 1000
]
# 2. Definir os Resultados correspondentes a cada condição
choices = [
    'Sem Avaliação',           # 0
    'Baixa Significância',     # 1-9
    'Significância Moderada',  # 10-99
    'Boa Significância',       # 100-999
    'Alta Significância'       # 1000+
]

notebook_data['reviews_count_category'] = np.select(conditions, choices, default='Indefinido')

#
notebook_data = (
        notebook_data[(notebook_data['new_price'] >= 500) 
        & 
        (notebook_data['new_price'] <= 10000)]
)
#Para explorar o DataFrame em um Notebook, se necessário.
notebook_data.to_csv(os.environ.get("CSV_FOLDER_PATH"), index=False)
print("DataFrame preparado.")


### -------------- CONFIGURANDO O BANCO DE DADOS -------------- ###

DRIVER = os.environ.get("DB_DRIVER")
SERVER_NAME = os.environ.get("DB_SERVER")
DATABASE_NAME = os.environ.get("DB_DATABASE")
UID = os.environ.get("DB_UID")
PWD = os.environ.get("DB_PWD")

# # --- Tentativa de Conexão Direta ---
# # Se esta linha falhar, o script vai quebrar aqui com um erro.
conn = pyodbc.connect(DRIVER=DRIVER, SERVER=SERVER_NAME, DATABASE=DATABASE_NAME, UID=UID, PWD=PWD, Encrypt='no')
# # Se o script chegar até aqui sem quebrar, a conexão foi estabelecida naquele instante.
print("\n>>> Sucesso! A linha pyodbc.connect() foi executada sem erro aparente.")


# #Configurando o Cursor
cursor = conn.cursor()
print("Cursor criado.")

NOME_TABELA = os.environ.get("NOME_TABELA")
SCHEMA_NAME = os.environ.get("SCHEMA_NAME")
print(f"Schema: {SCHEMA_NAME} | Tabela: {NOME_TABELA}")    

# # --- 2. SQL para Verificar a Existência da Tabela ---
# # Usamos OBJECT_ID para pegar o ID da tabela. Retorna NULL se não existir.
sql_check_table = f"SELECT OBJECT_ID(N'{SCHEMA_NAME}.{NOME_TABELA}', N'U');"

table_object_id = None

#Checando a existência da tabela.
# 1. Executa a consulta SQL que está em sql_check_table
cursor.execute(sql_check_table)
table_object_id = cursor.fetchone()

if table_object_id is not None:
    print(f"Tabela {SCHEMA_NAME}.{NOME_TABELA} existe e seu ID é: {table_object_id}.")
    print("Vamos inserir os dados...")

else:
    print(f"Tabela {SCHEMA_NAME}.{NOME_TABELA} não existe, e será criada...")
    sql_create_table = f"""
    CREATE TABLE {SCHEMA_NAME}.{NOME_TABELA} (
        -- Chave Primária Auto-Incremento (Boa prática)
        ID_PK INT PRIMARY KEY IDENTITY(1,1),
        
        -- Colunas Originais do DataFrame
        brand NVARCHAR(100) NULL,          -- Marcas (NVARCHAR para Unicode)
        name NVARCHAR(500) NULL,           -- Nomes/descrições (Aumente se precisar)
        reviews_rating DECIMAL(3, 1) NULL, -- Nota de avaliação (ex: 4.5)
        reviews_count INT NULL,            -- Quantidade de avaliações
        old_price DECIMAL(18, 2) NULL,     -- Preço antigo (precisão monetária)
        new_price DECIMAL(18, 2) NULL,     -- Preço novo (precisão monetária)
        source NVARCHAR(255) NULL,         -- Fonte dos dados (ex: nome do site)
        created_at DATETIME2 NULL,         -- Data/hora da coleta (preciso)

        -- Colunas Calculadas no DataFrame:

        discount DECIMAL(18, 2) NULL,       -- Total de desconto (ex: 150.50)
        rating_category NVARCHAR(50) NULL, -- Categoria da nota (ex: 'Excelente')
        reviews_count_category NVARCHAR(50) NULL, -- Categoria da contagem (ex: 'Contagem Alta (>Q3)')

        -- Coluna de Metadados (Boa prática):

        LoadDate DATETIME2 DEFAULT GETDATE() NULL -- Registra quando a linha foi inserida no banco
    );
    """
    # Executa o SQL para criar a tabela
    cursor.execute(sql_create_table)
    conn.commit()

columns_to_insert = ['brand', 'name', 'reviews_rating', 'reviews_count', 'old_price', 'new_price', 'source', 'created_at', 'discount', 'rating_category', 'reviews_count_category']

# Gera a parte "[col1], [col2], ..." a partir da lista explícita
colunas_sql = ', '.join([f'[{col}]' for col in columns_to_insert]) 

# Gera a parte "?, ?, ..." com o número correto de placeholders
placeholders_sql = ', '.join(['?'] * len(columns_to_insert))

sql_insert = f"""INSERT INTO {SCHEMA_NAME}.{NOME_TABELA} ({colunas_sql}) VALUES ({placeholders_sql});"""

print("Template SQL INSERT preparado.")

data_tuples = [tuple(x) for x in notebook_data[columns_to_insert].astype(object).replace({pd.NA: None, np.nan: None}).values]

# Executa o SQL de inserção para cada linha do DataFrame.
cursor.executemany(sql_insert, data_tuples) 

# Ação ESSENCIAL: Salva permanentemente todas as inserções no banco
conn.commit()

#Fechando o cursor e a conexão
cursor.close()
conn.close()
print("Conexão encerrada.")
print(">>> ETL concluído com sucesso!")