import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Inicializar o Faker
fake = Faker('pt_BR') 

# --- Configurações de Volume e Tempo ---
N_CUSTOMERS = 10000 
N_PRODUCTS = 200     
N_ORDERS = 100000    
START_DATE = datetime.now() - timedelta(days=730) 
END_DATE = datetime.now()
OUTPUT_DIR = 'data' # Pasta de saída

# --- Configuração de Pesos das Cidades (Garantindo soma = 1.0) ---
CITY_WEIGHTS_BASE = {
    'São Paulo': 30, 
    'Rio de Janeiro': 20,
    'Belo Horizonte': 10,
    'Porto Alegre': 5,
    'Salvador': 5,
}
outras_cidades_weight = 30 / 10
outras_cidades = {}
while len(outras_cidades) < 10:
    new_city = fake.city()
    if new_city not in CITY_WEIGHTS_BASE and new_city not in outras_cidades:
        outras_cidades[new_city] = outras_cidades_weight

CITY_WEIGHTS = {**CITY_WEIGHTS_BASE, **outras_cidades}
total_weight = sum(CITY_WEIGHTS.values()) 
CITIES = list(CITY_WEIGHTS.keys())
P_CITIES = np.array(list(CITY_WEIGHTS.values())) / total_weight 
# -----------------------------------------------------------------

# 1. Geração da Tabela products (200 linhas)
print("Gerando products...")
categories = ['Eletrônicos', 'Vestuário', 'Livros', 'Alimentos', 'Casa & Decoração']
category_prices = { 
    'Eletrônicos': (500.00, 5000.00),
    'Vestuário': (50.00, 300.00),
    'Livros': (20.00, 100.00),
    'Alimentos': (10.00, 80.00),
    'Casa & Decoração': (150.00, 1200.00)
}

products_data = []
for product_id in range(1, N_PRODUCTS + 1):
    category = np.random.choice(categories)
    min_price, max_price = category_prices[category]
    price = round(random.uniform(min_price, max_price), 2) 
    
    products_data.append({
        'product_id': product_id,
        'name': f"{category} - Produto {product_id}",
        'category': category,
        'price': price
    })
df_products = pd.DataFrame(products_data)

# 2. Geração da Tabela customers (10.000 linhas)
print("Gerando customers...")
def generate_customer(customer_id):
    name = fake.name()
    return {
        'customer_id': customer_id,
        'name': name,
        'email': f"cliente_{customer_id}_{fake.user_name()}@{fake.domain_name()}", 
        'city': np.random.choice(CITIES, p=P_CITIES), 
        'created_at': fake.date_between_dates(date_start=datetime.now() - timedelta(days=1825), date_end=datetime.now()).strftime('%Y-%m-%d')
    }
df_customers = pd.DataFrame([generate_customer(i) for i in range(1, N_CUSTOMERS + 1)])

# 3. Geração da Tabela orders (100.000 linhas)
print("Gerando orders...")
valid_customer_ids = df_customers['customer_id'].tolist()
valid_product_ids = df_products['product_id'].tolist()

def generate_order(order_id):
    order_date = fake.date_time_between_dates(datetime_start=START_DATE, datetime_end=END_DATE)
    customer_id = np.random.choice(valid_customer_ids, 
                                   p=np.repeat(1/N_CUSTOMERS, N_CUSTOMERS))

    return {
        'order_id': order_id,
        'customer_id': customer_id,
        'product_id': np.random.choice(valid_product_ids),
        'quantity': np.random.randint(1, 6), 
        'order_date': order_date.strftime('%Y-%m-%d')
    }
df_orders = pd.DataFrame([generate_order(i) for i in range(1, N_ORDERS + 1)])

# 4. Salvando os dados em CSVs
print("Salvando arquivos CSV...")
os.makedirs(OUTPUT_DIR, exist_ok=True) 
df_customers.to_csv(f'{OUTPUT_DIR}/customers.csv', index=False)
df_products.to_csv(f'{OUTPUT_DIR}/products.csv', index=False)
df_orders.to_csv(f'{OUTPUT_DIR}/orders.csv', index=False)

print("\n✅ Geração de dados concluída!")
print(f"Arquivos salvos em /{OUTPUT_DIR}/.")