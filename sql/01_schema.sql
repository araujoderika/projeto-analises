-- ============================================================
-- SCHEMA: Premium Motors — Sistema de Vendas Multi-Filial
-- ============================================================
-- Este script cria a estrutura do banco de dados. Rode este
-- arquivo primeiro, e depois o dados_inserts.sql.

CREATE TABLE IF NOT EXISTS filiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vendedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    filial_id INTEGER,
    FOREIGN KEY (filial_id) REFERENCES filiais(id)
);

CREATE TABLE IF NOT EXISTS carros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATE NOT NULL,
    preco_venda REAL NOT NULL,
    desconto REAL DEFAULT 0,
    filial_id INTEGER,
    vendedor_id INTEGER,
    carro_id INTEGER,
    cliente_id INTEGER,
    FOREIGN KEY (filial_id) REFERENCES filiais(id),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id),
    FOREIGN KEY (carro_id) REFERENCES carros(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
