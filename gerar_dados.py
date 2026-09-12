import os
import random
import sqlite3
from datetime import datetime, timedelta

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
banco_path = os.path.join(diretorio_atual, 'premium_motors.db')

conn = sqlite3.connect(banco_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM vendas")

filiais_ids = [1, 2, 3]
vendedores_ids = [1, 2, 3]
carros_ids = [1, 2, 3]
clientes_ids = [1, 2, 3]

precios_base = {
    1: 850000.00,
    2: 600000.00,
    3: 210000.00
}

data_inicio = datetime(2025, 1, 1)
data_fim = datetime(2025, 12, 31)
dias_totais = (data_fim - data_inicio).days

vendas = []
for _ in range(130):
    dias_aleatorios = random.randint(0, dias_totais)
    data_venda = (data_inicio + timedelta(days=dias_aleatorios)).strftime('%Y-%m-%d')

    carro_id = random.choice(carros_ids)
    preco_tabela = precios_base[carro_id]

    desconto = round(preco_tabela * random.uniform(0.0, 0.05), 2) if random.random() > 0.6 else 0.0
    preco_venda = preco_tabela - desconto

    filial_id = random.choice(filiais_ids)
    vendedor_id = random.choice(vendedores_ids)
    cliente_id = random.choice(clientes_ids)

    vendas.append((data_venda, preco_venda, desconto, filial_id, vendedor_id, carro_id, cliente_id))

cursor.executemany("""
    INSERT INTO vendas (data_venda, preco_venda, desconto, filial_id, vendedor_id, carro_id, cliente_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", vendas)

conn.commit()
conn.close()

print("✅ 130 vendas sintéticas geradas e inseridas com sucesso!")
