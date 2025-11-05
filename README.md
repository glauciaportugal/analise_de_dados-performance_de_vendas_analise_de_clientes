# Teste Técnico - Analista de Dados | Alymente

## 1. Visão Geral do Projeto

 Este projeto visa analisar a performance de vendas, produtos e clientes, conforme os requisitos do teste técnico.

### Ferramentas Utilizadas
* **Geração de Dados:** Python (Pandas, Numpy, Faker)
* **Tecnologias:** Google BigQuery SQL  e SQLTools (para testes em SQLite no VS Code).
* **Carregamento (ETL):** Python (`google-cloud-bigquery`)
* **Visualização e Dashboard:** Power BI Desktop

###  Principais Decisões  

| Decisão | Justificativa |
| :--- | :--- |
| **Geração de Dados Sintéticos** | Devido ao requisito de volume (~10k clientes, 200 produtos, 100k pedidos) e a necessidade de incluir variação de preços por categoria e volumes de vendas por cidade. |
| **Análise (Parte 1)** | A análise foi realizada no **BigQuery** para simular um ambiente de produção em nuvem. As consultas em `scripts.sql` estão otimizadas para o BigQuery SQL. |
| **Modelagem de Dados** |  O modelo de dados é composto por três tabelas relacionais (esquema estrela ): `customers`, `products` e `orders`. |

---

## 2. Dicionário de Dados (Estrutura das Tabelas)

### ➡️ Tabela `customers` (Clientes)

| Coluna | Tipo de Dado | Chave/Relação | Descrição |
| :--- | :--- | :--- | :--- |
| `customer_id` | INT | PRIMARY KEY | Identificador único do cliente. |
| `name` |  VARCHAR(100) | | Nome completo do cliente. |
| `email` |  VARCHAR(100) | | Endereço de e-mail do cliente. |
| `city` |  VARCHAR(100)  | |  Cidade de residência (Usado para análise de volume ). |
| `created_at` |  DATE | | Data de cadastro do cliente. |

### ➡️ Tabela `products` (Produtos)

| Coluna | Tipo de Dado | Chave/Relação | Descrição |
| :--- | :--- | :--- | :--- |
| `product_id` | INT |  PRIMARY KEY  | Identificador único do produto. |
| `name` |  VARCHAR(100)  | | Nome do produto. |
| `category` |  VARCHAR(100) | | Categoria do produto (Usado para variação de preço/receita ). |
| `price` | DECIMAL(10, 2)  | | Preço unitário atual do produto. |

### ➡️ Tabela `orders` (Pedidos/Transações)

| Coluna | Tipo de Dado | Chave/Relação | Descrição |
| :--- | :--- | :--- | :--- |
| `order_id` | INT | PRIMARY KEY  | Identificador único do pedido/transação. |
| `customer_id` | INT | FOREIGN KEY (FK)  | Chave que referencia a tabela `customers`. |
| `product_id` | INT | FOREIGN KEY (FK)  | Chave que referencia a tabela `products`. |
| `quantity` | INT  | | Quantidade de unidades vendidas do produto no pedido. |
| `order_date` | DATE | | Data e hora em que o pedido foi realizado. |

---

## 3. Instruções de Entrega e Reprodução [cite: 84]

### A. Geração e Carregamento de Dados
1. O repositório inclui os scripts `data_generator.py` e `upload_to_bigquery.py`.
2. O script de upload cria as tabelas no BigQuery (Projeto: `tech-challenge-03`, Dataset: `teste_analista_vendas`).

### B. Para Executar a Análise SQL
1. O arquivo **`scripts.sql`** contém todas as 6 consultas finais.
2. O código é otimizado para o BigQuery SQL.

 ---

## 4. 📊 Dashboard (Link de Entrega)

O dashboard criado no Power BI pode ser acessado publicamente através do link abaixo:

**Link de Acesso Público:** [Alymente - Performance de Vendas](https://app.powerbi.com/links/Jso2jYg9wN?ctid=61ce4849-f431-4bc1-ae22-0e4c1b6ebc14&pbi_source=linkShare)

---

## 5. 🎯 Storytelling: Insights e Recomendações (Narrativa Final)

**Parágrafo 1: Visão Geral e Força Motriz (Faturamento)**
> "A performance de vendas da Alymente demonstra uma dependência significativa da categoria **Eletrônicos**, que sozinha é responsável por mais de 72% da receita total. O faturamento é impulsionado por um grupo concentrado de clientes nas cidades de São Paulo e Rio de Janeiro, que, juntas, representam uma grande fatia do total. O sucesso do negócio está, ligado à retenção dos clientes de alto valor nestes dois mercados primários."

**Parágrafo 2: Tendência, Oportunidade e Risco**
> "A análise de frequência revela um padrão de compra recorrente em produtos de menor valor, mas maior volume. As categorias Vestuário e Alimentos elevam a retenção do cliente no canal de vendas, evidenciando um ciclo de recompra mais rápido e consistente para itens essenciais ou de uso contínuo. Nosso Ciclo Médio de Recompra global de 62 dias deve ser segmentado: enquanto Eletrônicos gera valor, Vestuário e Alimentos geram a fidelidade e o fluxo de transações."

**Parágrafo 3: Recomendações Estratégicas (Ação)**
> "Recomendamos três ações estratégicas imediatas: 1) Focar na Recorrência: Criar estratégias de fidelização para as categorias Vestuário e Alimentos, capitalizando o alto volume e frequência para aumentar o Ticket Médio nesses segmentos. 2) Retenção de Valor: Implementar uma campanha de reengajamento direcionada a clientes de alto valor que compram Eletrônicos, caso ultrapassem 75 dias sem compra (risco de churn). 3) Otimização Geográfica: Manter o foco de investimento em São Paulo e Rio de Janeiro, mas explorar estratégias para aumentar o volume de pedidos em cidades com ticket médio elevado."
