-- ============================================================
-- ANÁLISE DE VENDAS — Premium Motors
-- Cada bloco abaixo responde a uma pergunta real que a diretoria
-- comercial faria no dia a dia.
-- ============================================================

-- ------------------------------------------------------------
-- 1) Qual foi o faturamento total e o ticket médio no período?
-- ------------------------------------------------------------
SELECT
    COUNT(*) AS total_vendas,
    ROUND(SUM(preco_final), 2) AS faturamento_total,
    ROUND(AVG(preco_final), 2) AS ticket_medio
FROM vendas;

-- ------------------------------------------------------------
-- 2) Quais os 3 vendedores que mais faturaram?
--    (útil para identificar top performers e premiar bons resultados)
-- ------------------------------------------------------------
SELECT
    v.nome AS vendedor,
    COUNT(*) AS carros_vendidos,
    ROUND(SUM(vd.preco_final), 2) AS faturamento
FROM vendas vd
JOIN vendedores v ON vd.id_vendedor = v.id
GROUP BY v.nome
ORDER BY faturamento DESC
LIMIT 3;

-- ------------------------------------------------------------
-- 3) Qual filial fatura mais? Qual vende mais UNIDADES?
--    (uma filial pode faturar mais vendendo poucos carros caros,
--     outra pode vender muitos carros baratos — os dois números
--     juntos contam a história completa)
-- ------------------------------------------------------------
SELECT
    f.nome AS filial,
    COUNT(*) AS unidades_vendidas,
    ROUND(SUM(vd.preco_final), 2) AS faturamento
FROM vendas vd
JOIN carros c ON vd.id_carro = c.id
JOIN filiais f ON c.id_filial = f.id
GROUP BY f.nome
ORDER BY faturamento DESC;

-- ------------------------------------------------------------
-- 4) Qual categoria de carro (Sedan, SUV, Hatch...) mais gera
--    receita? É onde vale a pena investir mais estoque.
-- ------------------------------------------------------------
SELECT
    c.categoria,
    COUNT(*) AS unidades_vendidas,
    ROUND(SUM(vd.preco_final), 2) AS faturamento,
    ROUND(AVG(vd.preco_final), 2) AS ticket_medio_categoria
FROM vendas vd
JOIN carros c ON vd.id_carro = c.id
GROUP BY c.categoria
ORDER BY faturamento DESC;

-- ------------------------------------------------------------
-- 5) Quais carros estão parados em estoque (nunca vendidos)?
--    Sinaliza excesso de estoque parado / capital empatado.
-- ------------------------------------------------------------
SELECT
    c.categoria,
    COUNT(*) AS unidades_paradas,
    ROUND(SUM(c.preco_tabela), 2) AS valor_parado_em_estoque
FROM carros c
WHERE c.em_estoque = 1
GROUP BY c.categoria
ORDER BY valor_parado_em_estoque DESC;

-- ------------------------------------------------------------
-- 6) Qual foi a evolução do faturamento mês a mês em 2025?
--    (base para identificar sazonalidade e planejar metas)
-- ------------------------------------------------------------
SELECT
    substr(data_venda, 1, 7) AS mes,
    COUNT(*) AS vendas_no_mes,
    ROUND(SUM(preco_final), 2) AS faturamento_no_mes
FROM vendas
GROUP BY mes
ORDER BY mes;

-- ------------------------------------------------------------
-- 7) Qual o desconto médio concedido por vendedor?
--    (vendedores que dão muito desconto reduzem a margem —
--     importante pra política comercial)
-- ------------------------------------------------------------
SELECT
    vend.nome AS vendedor,
    ROUND(AVG(1 - (vd.preco_final / c.preco_tabela)) * 100, 2) AS desconto_medio_percentual
FROM vendas vd
JOIN carros c ON vd.id_carro = c.id
JOIN vendedores vend ON vd.id_vendedor = vend.id
GROUP BY vend.nome
ORDER BY desconto_medio_percentual DESC;

-- ------------------------------------------------------------
-- 8) De quais cidades vêm os clientes que mais compram?
--    (ajuda a decidir onde investir em marketing regional)
-- ------------------------------------------------------------
SELECT
    cl.cidade,
    COUNT(*) AS total_compras,
    ROUND(SUM(vd.preco_final), 2) AS valor_total
FROM vendas vd
JOIN clientes cl ON vd.id_cliente = cl.id
GROUP BY cl.cidade
ORDER BY valor_total DESC;

-- ------------------------------------------------------------
-- 9) Ranking completo de vendedores com sua filial
--    (visão gerencial para avaliação de desempenho por equipe)
-- ------------------------------------------------------------
SELECT
    f.nome AS filial,
    vend.nome AS vendedor,
    COUNT(*) AS carros_vendidos,
    ROUND(SUM(vd.preco_final), 2) AS faturamento
FROM vendas vd
JOIN vendedores vend ON vd.id_vendedor = vend.id
JOIN filiais f ON vend.id_filial = f.id
GROUP BY f.nome, vend.nome
ORDER BY f.nome, faturamento DESC;

-- ------------------------------------------------------------
-- 10) Qual foi o carro individual mais caro vendido no período,
--     e quem comprou?
-- ------------------------------------------------------------
SELECT
    cl.nome AS cliente,
    c.marca,
    c.modelo,
    vd.preco_final,
    vd.data_venda
FROM vendas vd
JOIN carros c ON vd.id_carro = c.id
JOIN clientes cl ON vd.id_cliente = cl.id
ORDER BY vd.preco_final DESC
LIMIT 1;
