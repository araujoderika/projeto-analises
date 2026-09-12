-- 1. Qual o faturamento total e o ticket médio?
SELECT
    SUM(preco_venda) AS faturamento_total,
    AVG(preco_venda) AS ticket_medio
FROM vendas;

-- 2. Quem são os 3 principais vendedores por faturamento?
SELECT
    v.nome AS vendedor,
    SUM(ven.preco_venda) AS faturamento
FROM vendas ven
JOIN vendedores v ON ven.vendedor_id = v.id
GROUP BY v.nome
ORDER BY faturamento DESC
LIMIT 3;

-- 3. Qual filial fatura mais / vende mais unidades?
SELECT
    f.nome AS filial,
    SUM(v.preco_venda) AS faturamento_total,
    COUNT(v.id) AS total_unidades
FROM vendas v
JOIN filiais f ON v.filial_id = f.id
GROUP BY f.nome
ORDER BY faturamento_total DESC;

-- 4. Qual categoria de carro gera mais receita?
SELECT
    c.categoria,
    SUM(v.preco_venda) AS faturamento,
    COUNT(v.id) AS unidades_vendidas
FROM vendas v
JOIN carros c ON v.carro_id = c.id
GROUP BY c.categoria
ORDER BY faturamento DESC;

-- 5. Quais carros estão parados em estoque (sem nenhuma venda)?
SELECT
    c.modelo,
    c.categoria,
    c.preco
FROM carros c
LEFT JOIN vendas v ON c.id = v.carro_id
WHERE v.id IS NULL;

-- 6. Como o faturamento evoluiu mês a mês?
SELECT
    strftime('%Y-%m', data_venda) AS mes,
    SUM(preco_venda) AS faturamento_mensal,
    COUNT(id) AS total_vendas
FROM vendas
GROUP BY mes
ORDER BY mes;

-- 7. Qual vendedor concede mais desconto em média?
SELECT
    v.nome AS vendedor,
    AVG(ven.desconto) AS media_desconto,
    SUM(ven.desconto) AS total_desconto
FROM vendas ven
JOIN vendedores v ON ven.vendedor_id = v.id
GROUP BY v.nome
ORDER BY media_desconto DESC;

-- 8. De quais cidades vêm os clientes que mais compram?
SELECT
    c.cidade,
    COUNT(v.id) AS total_compras,
    SUM(v.preco_venda) AS faturamento_por_cidade
FROM vendas v
JOIN clientes c ON v.cliente_id = c.id
GROUP BY c.cidade
ORDER BY faturamento_por_cidade DESC;

-- 9. Ranking de vendedores agrupados por filiais
SELECT
    f.nome AS filial,
    v.nome AS vendedor,
    SUM(ven.preco_venda) AS faturamento
FROM vendas ven
JOIN vendedores v ON ven.vendedor_id = v.id
JOIN filiais f ON ven.filial_id = f.id
GROUP BY f.nome, v.nome
ORDER BY f.nome, faturamento DESC;

-- 10. Qual foi a venda de maior valor do período?
SELECT
    v.id AS venda_id,
    v.data_venda,
    v.preco_venda,
    c.modelo AS carro,
    cli.nome AS cliente,
    vend.nome AS vendedor
FROM vendas v
JOIN carros c ON v.carro_id = c.id
JOIN clientes cli ON v.cliente_id = cli.id
JOIN vendedores vend ON v.vendedor_id = vend.id
ORDER BY v.preco_venda DESC
LIMIT 1;
