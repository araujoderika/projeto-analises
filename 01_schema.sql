-- ============================================================
-- SCHEMA: Premium Motors — Sistema de Vendas Multi-Filial
-- ============================================================
-- Este script cria a estrutura do banco de dados. Rode este
-- arquivo primeiro, e depois o dados_inserts.sql.

CREATE TABLE filiais (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    localizacao TEXT NOT NULL
);

CREATE TABLE vendedores (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    id_filial INTEGER NOT NULL,
    FOREIGN KEY (id_filial) REFERENCES filiais(id)
);

CREATE TABLE carros (
    id INTEGER PRIMARY KEY,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    categoria TEXT NOT NULL,       -- Sedan, SUV, Hatch, Esportivo, Picape
    preco_tabela REAL NOT NULL,
    id_filial INTEGER NOT NULL,    -- filial onde o carro está/estava em estoque
    em_estoque INTEGER NOT NULL,   -- 1 = disponível, 0 = já vendido
    FOREIGN KEY (id_filial) REFERENCES filiais(id)
);

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL
);

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY,
    id_carro INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_vendedor INTEGER NOT NULL,
    data_venda TEXT NOT NULL,      -- formato AAAA-MM-DD
    preco_final REAL NOT NULL,     -- preço após desconto negociado
    FOREIGN KEY (id_carro) REFERENCES carros(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id)
);
