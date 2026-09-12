import os
import sqlite3

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
banco_path = os.path.join(diretorio_atual, 'premium_motors.db')

conn = sqlite3.connect(banco_path)
cursor = conn.cursor()

def formatar_moeda(valor):
    if valor is None:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

print("=" * 60)
print("       RELATÓRIO DE NEGÓCIO — PREMIUM MOTORS")
print("=" * 60)

# 1. Total de vendas, faturamento total e ticket médio
cursor.execute("SELECT COUNT(*), SUM(preco_venda), AVG(preco_venda) FROM vendas")
total_vendas, faturamento_total, ticket_medio = cursor.fetchone()

print(f"\n📊 Total de vendas no período: {total_vendas}")
print(f"💰 Faturamento total: {formatar_moeda(faturamento_total)}")
print(f"🎫 Ticket médio: {formatar_moeda(ticket_medio)}")

# 2. Top 3 vendedores por faturamento
print("\n🏆 Top 3 vendedores por faturamento:")
query_top_vendedores = """
SELECT v.nome, SUM(ven.preco_venda) 
FROM vendas ven
JOIN vendedores v ON ven.vendedor_id = v.id
GROUP BY v.nome
ORDER BY SUM(ven.preco_venda) DESC
LIMIT 3
"""
cursor.execute(query_top_vendedores)
for nome, fat in cursor.fetchall():
    print(f"   - {nome}: {formatar_moeda(fat)}")

# 3. Faturamento por filial
print("\n🏢 Faturamento por filial:")
query_filiais = """
SELECT f.nome, SUM(v.preco_venda), COUNT(v.id)
FROM vendas v
JOIN filiais f ON v.filial_id = f.id
GROUP BY f.nome
ORDER BY SUM(v.preco_venda) DESC
"""
cursor.execute(query_filiais)
for nome, fat, qtd in cursor.fetchall():
    print(f"   - {nome}: {formatar_moeda(fat)} ({qtd} unidades)")

# 4. Receita por Categoria de Carro
print("\n🚗 Faturamento por Categoria de Carro:")
query_categorias = """
SELECT c.categoria, SUM(v.preco_venda), COUNT(v.id)
FROM vendas v
JOIN carros c ON v.carro_id = c.id
GROUP BY c.categoria
ORDER BY SUM(v.preco_venda) DESC
"""
cursor.execute(query_categorias)
for cat, fat, qtd in cursor.fetchall():
    print(f"   - {cat}: {formatar_moeda(fat)} ({qtd} unidades)")

conn.close()
print("\n" + "=" * 60)
