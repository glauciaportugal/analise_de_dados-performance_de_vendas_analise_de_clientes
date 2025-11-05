-- ##############################################
-- PARTE 1 - REQUISITOS SQL
-- Banco de Dados: SQLite (Testado no VS Code com SQLTools)
-- ##############################################

-- Métrica Base: total_spent é sempre (quantity * price)
-- --------------------------------------------------------------------------------

-- 1) Top clientes
-- Requisito: Liste os 10 clientes que mais gastaram no total.
-- Saída: customer_id, name, total_spent, total_orders, avg_ticket
SELECT
    c.customer_id,
    c.name,
    SUM(o.quantity * p.price) AS total_spent,
    COUNT(DISTINCT o.order_id) AS total_orders,
     CAST(SUM(o.quantity * p.price) AS REAL) / COUNT(DISTINCT o.order_id) AS avg_ticket
FROM
    orders o
INNER JOIN
    products p ON o.product_id = p.product_id
INNER JOIN
    customers c ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY
    total_spent DESC
LIMIT 10;

-- --------------------------------------------------------------------------------

-- 2) Vendas por categoria
-- Requisito: Retorne receita total e quantidade total vendida por categoria.
-- Saída: category, total_revenue, total_quantity, avg_price
SELECT
    p.category,
    SUM(o.quantity * p.price) AS total_revenue,
    SUM(o.quantity) AS total_quantity,
    -- Preço médio ponderado pelo volume de vendas  
    CAST(SUM(o.quantity * p.price) AS REAL) / SUM(o.quantity) AS avg_price
FROM
    orders o
INNER JOIN
    products p ON o.product_id = p.product_id
GROUP BY
    p.category
ORDER BY
    total_revenue DESC;

-- --------------------------------------------------------------------------------

-- 3) Média de ticket por cidade
-- Requisito: Ticket médio por pedido em cada cidade.
-- Saída: city, total_revenue, total_orders, avg_ticket
SELECT
    c.city,
    SUM(o.quantity * p.price) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    CAST(SUM(o.quantity * p.price) AS REAL) / COUNT(DISTINCT o.order_id) AS avg_ticket
FROM
    orders o
INNER JOIN
    products p ON o.product_id = p.product_id
INNER JOIN
    customers c ON o.customer_id = c.customer_id
GROUP BY
    c.city
HAVING
    total_orders > 0 -- Garante que apenas cidades com pedidos válidos sejam consideradas
ORDER BY
    avg_ticket DESC;

-- --------------------------------------------------------------------------------

-- 4) Evolução das vendas
-- Requisito: Receita total por mês nos últimos 12 meses.
-- Saída: year_month (YYYY-MM), total_revenue, total_orders

 
WITH BaseCalculations AS (
    -- Calcula o gasto por linha de pedido e extrai o YYYY-MM
    SELECT
        strftime('%Y-%m', o.order_date) AS year_month,
        o.order_date,
        o.order_id,
        (o.quantity * p.price) AS total_spent
    FROM
        orders o
    INNER JOIN
        products p ON o.product_id = p.product_id
),
DateRange AS (
    -- Encontra a data mais recente e define o ponto de corte (12 meses antes)
    SELECT
        strftime('%Y-%m-%d', MAX(order_date), '-12 month') AS start_date
    FROM
        orders
)
SELECT
    T1.year_month,
    SUM(T1.total_spent) AS total_revenue,
    COUNT(DISTINCT T1.order_id) AS total_orders
FROM
    BaseCalculations T1
CROSS JOIN
    DateRange T2
WHERE
    -- Filtra para incluir apenas os últimos 12 meses
    T1.order_date >= T2.start_date
GROUP BY
    T1.year_month
ORDER BY
    T1.year_month ASC;

-- --------------------------------------------------------------------------------

-- 5) Produto com maior crescimento (mês a mês)
-- Requisito: Produto com maior taxa média de crescimento percentual no último semestre (6 meses).
-- Saída: product_id, name, month_from, month_to, qty_from, qty_to, growth_absolute, growth_pct

-- NOTA: SQLite NÃO suporta a função LAG() diretamente em versões mais antigas. 
-- Para compatibilidade garantida, esta consulta é mais complexa ou requer uma CTE recursiva/auto-join.
-- No entanto, o código abaixo usa a sintaxe padrão de Funções de Janela (disponível no SQLite 3.25.0+):

WITH MonthlySales AS (
    SELECT
        p.product_id,
        p.name,
        strftime('%Y-%m', o.order_date) AS year_month,
        SUM(o.quantity) AS qty_current_month
    FROM
        orders o
    INNER JOIN
        products p ON o.product_id = p.product_id
    WHERE
        o.order_date >= strftime('%Y-%m-%d', 'now', '-6 month') -- Últimos 6 meses
    GROUP BY
        1, 2, 3
),
GrowthCalculation AS (
    -- Uso da função de janela LAG para obter a quantidade do mês anterior
    SELECT
        product_id,
        name,
        year_month AS month_to,
        qty_current_month,
        LAG(qty_current_month, 1, 0) OVER (PARTITION BY product_id ORDER BY year_month) AS qty_previous_month
    FROM
        MonthlySales
),
GrowthRates AS (
    -- Calcula as taxas de crescimento e exclui o primeiro mês de cada produto (mês incompleto/sem base)
    SELECT
        product_id,
        name,
        month_to,
        LAG(month_to, 1, 'N/A') OVER (PARTITION BY product_id ORDER BY month_to) AS month_from,
        qty_current_month AS qty_to,
        qty_previous_month AS qty_from,
        (qty_current_month - qty_previous_month) AS growth_absolute,
        CASE
            WHEN qty_previous_month > 0 THEN CAST((qty_current_month - qty_previous_month) AS REAL) / qty_previous_month
            ELSE 0 -- Trata divisão por zero (mês anterior com 0 vendas)
        END AS growth_pct
    FROM
        GrowthCalculation
    WHERE
        qty_previous_month > 0 -- Filtra o primeiro mês de cada produto com vendas
)
-- Retorna o produto com a maior taxa MÉDIA de crescimento percentual
SELECT
    product_id,
    name,
    AVG(growth_pct) AS avg_growth_pct,
    SUM(growth_absolute) AS total_growth_absolute
FROM
    GrowthRates
GROUP BY
    product_id,
    name
ORDER BY
    avg_growth_pct DESC
LIMIT 1;

-- --------------------------------------------------------------------------------

-- 6) Clientes inativos
-- Requisito: Clientes que não compraram nos últimos 3 meses, incluindo quem nunca comprou.
-- Saída: customer_id, name, email, city, last_order_date
-- NOTA: SQLite usa o 'current_date' ou 'now'

-- 6) Clientes inativos (CORRIGIDO PARA SQLITE)

WITH LastOrder AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date
    FROM
        orders
    GROUP BY
        customer_id
),
InactivityThreshold AS (
    -- Define o limite de 3 meses atrás (função SQLite)
    SELECT
        strftime('%Y-%m-%d', 'now', '-3 month') AS threshold_date
)
SELECT
    c.customer_id,
    c.name,
    c.email,
    c.city,
    lo.last_order_date
FROM
    customers c
LEFT JOIN
    LastOrder lo ON c.customer_id = lo.customer_id
CROSS JOIN
    InactivityThreshold t
WHERE
    -- Condição 1: A última data de pedido é mais antiga que o limite de 3 meses
    (lo.last_order_date < t.threshold_date)
    -- Condição 2: OU o cliente NUNCA comprou (last_order_date é NULL)
    OR (lo.last_order_date IS NULL)
ORDER BY
    -- Coloca NULLS (clientes que nunca compraram) no topo (TRUE é 1, FALSE é 0)
    (lo.last_order_date IS NULL) DESC,
    lo.last_order_date DESC;