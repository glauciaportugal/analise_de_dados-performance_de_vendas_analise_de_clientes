from google.cloud import bigquery
import os

# --- Configurações do Projeto ---
PROJECT_ID = "tech-challenge-03"
DATASET_ID = "teste_analista_vendas"
CSV_PATH = "data/"
TABLES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv"
}

def upload_csv_to_bigquery(table_id, csv_file_name, client):
    """Carrega um arquivo CSV no BigQuery."""
    
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"
    file_path = os.path.join(CSV_PATH, csv_file_name)

    # 1. Configurar o Job de Carregamento
    job_config = bigquery.LoadJobConfig(
        # Informa ao BigQuery para inferir o esquema (nomes e tipos de colunas)
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        # O CSV não tem cabeçalho (já que o pandas não exporta com índice)
        skip_leading_rows=1, 
    )

    # 2. Abrir o arquivo localmente e iniciar o Job
    try:
        with open(file_path, "rb") as source_file:
            print(f"Iniciando upload de {csv_file_name} para {table_id}...")
            job = client.load_table_from_file(
                source_file,
                table_ref,
                job_config=job_config
            )
        
        # 3. Esperar que o Job termine
        job.result() 
        print(f"✅ Sucesso! Tabela {table_id} carregada. {job.output_rows} linhas inseridas.")
        
    except Exception as e:
        print(f"❌ Erro ao carregar a tabela {table_id}: {e}")
        # Se as tabelas já existirem, este job pode falhar (a não ser que você adicione if_exists=replace)


# --- Execução Principal ---
if __name__ == "__main__":
    
    # Instancia o cliente BigQuery
    client = bigquery.Client(project=PROJECT_ID)

    print(f"Conectando ao BigQuery no projeto: {PROJECT_ID}")
    
    # 1. Garante que o Dataset exista
    try:
        client.get_dataset(DATASET_ID)
    except Exception:
        print(f"Dataset {DATASET_ID} não encontrado. Criando...")
        dataset = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
        client.create_dataset(dataset, exists_ok=True)


    # 2. Roda o upload para cada tabela
    for table_id, csv_name in TABLES.items():
        # Para fins de teste, você pode querer recriar a tabela a cada execução
        # Para produção, você deve verificar a existência da tabela.
        upload_csv_to_bigquery(table_id, csv_name, client)

    print("\nProcesso de upload para o BigQuery concluído.")