import pandas as pd
import sqlite3
import os

# Caminho dos dados (assumindo que a pasta 'data' está na raiz)
CSV_PATH = 'data/'
DB_FILE = 'sales_data.db'

# Carregar os dados dos CSVs
df_customers = pd.read_csv(os.path.join(CSV_PATH, 'customers.csv'))
df_products = pd.read_csv(os.path.join(CSV_PATH, 'products.csv'))
df_orders = pd.read_csv(os.path.join(CSV_PATH, 'orders.csv'))

# 2. Conectar e criar o banco de dados
conn = sqlite3.connect(DB_FILE)
print(f"Conexão com o banco de dados '{DB_FILE}' estabelecida.")

# 3. Exportar DataFrames para Tabelas SQL
# 'if_exists=replace' garante que se a tabela existir, ela será recriada.
df_customers.to_sql('customers', conn, if_exists='replace', index=False)
df_products.to_sql('products', conn, if_exists='replace', index=False)
df_orders.to_sql('orders', conn, if_exists='replace', index=False)

conn.close()
print("As tabelas (customers, products, orders) foram criadas e populadas com sucesso no SQLite!")