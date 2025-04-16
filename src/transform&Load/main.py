import pandas as pd
import datetime
import pyodbc

pd.options.display.max_columns = None
notebook_data = pd.read_json("data\data.json")

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

#CONFIGURANDO O BANCO DE DADOS

DRIVER = "ODBC Driver 18 for SQL Server"
SERVER_NAME = "TREVIS"
DATABASE_NAME = "MercadoLivreNotebooksDW"
UID = "ETL_USER"
PWD = "0y3Ysr3ICZYNcMZgTvjd"

# --- Tentativa de Conexão Direta ---
# Se esta linha falhar, o script vai quebrar aqui com um erro.
conn = pyodbc.connect(DRIVER=DRIVER, SERVER=SERVER_NAME, DATABASE=DATABASE_NAME, UID=UID, PWD=PWD, Encrypt='no')

# Se o script chegar até aqui sem quebrar, a conexão foi estabelecida naquele instante.
print("\n>>> Sucesso! A linha pyodbc.connect() foi executada sem erro aparente.")
print(">>> IMPORTANTE: A conexão NÃO foi fechada e NENHUM erro foi tratado.")