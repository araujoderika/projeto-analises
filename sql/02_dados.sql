INSERT INTO filiais (nome) VALUES 
('Premium Motors - Barueri'),
('Premium Motors - Campinas'),
('Premium Motors - Osasco');

INSERT INTO vendedores (nome, filial_id) VALUES 
('Patrícia Gomes', 1),
('Camila Rocha', 2),
('Lucas Martins', 3);

INSERT INTO carros (modelo, categoria, preco) VALUES 
('Porsche 911', 'Esportivo', 850000.00),
('BMW M3', 'Esportivo', 600000.00),
('Golf GTI', 'Hatch', 210000.00);

INSERT INTO clientes (nome, cidade) VALUES 
('Carlos Silva', 'São Paulo'),
('Ana Souza', 'Campinas'),
('Roberto Alves', 'Barueri');

INSERT INTO vendas (data_venda, preco_venda, desconto, filial_id, vendedor_id, carro_id, cliente_id) VALUES 
('2025-02-15', 850000.00, 0, 1, 1, 1, 1),
('2025-02-18', 600000.00, 10000, 2, 2, 2, 2),
('2025-03-01', 200000.00, 10000, 3, 3, 3, 3);
