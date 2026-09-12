import os
import sqlite3

# 1. Ajusta os caminhos
diretorio_script = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(diretorio_script) == 'sql':
    raiz_projeto = os.path.dirname(diretorio_script)
else:
    raiz_projeto = diretorio_script

banco_path = os.path.join(raiz_projeto, 'premium_motors.db')
pasta_sql = os.path.join(raiz_projeto, 'sql')

conn = sqlite3.connect(banco_path)
cursor = conn.cursor()

# 2. Garante a criação do banco e carga inicial
for arq in ['01_schema.sql', '02_dados.sql']:
    caminho_arq = os.path.join(pasta_sql, arq)
    if os.path.exists(caminho_arq):
        with open(caminho_arq, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
conn.commit()

def formatar_moeda(valor):
    if valor is None:
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

print("=" * 65)
print("       RELATÓRIO COMPLETO DE NEGÓCIO (10 ANÁLISES) — PREMIUM MOTORS")
print("=" * 65)

# 1. Faturamento Total e Ticket Médio
cursor.execute("SELECT SUM(preco_venda), AVG(preco_venda), COUNT(*) FROM vendas")
fat_total, ticket_medio, total_vendas = cursor.fetchone()
print(f"\n1. 📊 Faturamento Total: {formatar_moeda(fat_total)} | Ticket Médio: {formatar_moeda(ticket_medio)} | Total Vendas: {total_vendas}")

# 2. Top 3 Vendedores
print("\n2. 🏆 Top 3 Vendedores por Faturamento:")
cursor.execute("""
    SELECT v.nome, SUM(ven.preco_venda) 
    FROM vendas ven JOIN vendedores v ON ven.vendedor_id = v.id
    GROUP BY v.nome ORDER BY SUM(ven.preco_venda) DESC LIMIT 3
""")
for nome, fat in cursor.fetchall():
    print(f"   - {nome}: {formatar_moeda(fat)}")

# 3. Desempenho por Filial
print("\n3. 🏢 Desempenho por Filial:")
cursor.execute("""
    SELECT f.nome, SUM(v.preco_venda), COUNT(v.id)
    FROM vendas v JOIN filiais f ON v.filial_id = f.id
    GROUP BY f.nome ORDER BY SUM(v.preco_venda) DESC
""")
for nome, fat, qtd in cursor.fetchall():
    print(f"   - {nome}: {formatar_moeda(fat)} ({qtd} un.)")

# 4. Receita por Categoria
print("\n4. 🚗 Receita por Categoria de Veículo:")
cursor.execute("""
    SELECT c.categoria, SUM(v.preco_venda), COUNT(v.id)
    FROM vendas v JOIN carros c ON v.carro_id = c.id
    GROUP BY c.categoria ORDER BY SUM(v.preco_venda) DESC
""")
for cat, fat, qtd in cursor.fetchall():
    print(f"   - {cat}: {formatar_moeda(fat)} ({qtd} un.)")

# 5. Estoque Parado
print("\n5. ⚠️ Carros sem Vendas Registradas (Estoque Parado):")
cursor.execute("""
    SELECT c.modelo, c.preco FROM carros c
    LEFT JOIN vendas v ON c.id = v.carro_id WHERE v.id IS NULL
""")
carros_parados = cursor.fetchall()
if carros_parados:
    for mod, preco in carros_parados:
        print(f"   - {mod} (Valor Tabela: {formatar_moeda(preco)})")
else:
    print("   - Nenhum modelo totalmente parado no momento.")

# 6. Evolução Mês a Mês
print("\n6. 📅 Evolução Mensal do Faturamento:")
cursor.execute("""
    SELECT strftime('%Y-%m', data_venda) AS mes, SUM(preco_venda), COUNT(id)
    FROM vendas GROUP BY mes ORDER BY mes
""")
for mes, fat, qtd in cursor.fetchall():
    print(f"   - Mês {mes}: {formatar_moeda(fat)} ({qtd} vendas)")

# 7. Média de Descontos por Vendedor
print("\n7. 🏷️ Desconto Médio Concedido por Vendedor:")
cursor.execute("""
    SELECT v.nome, AVG(ven.desconto)
    FROM vendas ven JOIN vendedores v ON ven.vendedor_id = v.id
    GROUP BY v.nome ORDER BY AVG(ven.desconto) DESC
""")
for nome, desc_medio in cursor.fetchall():
    print(f"   - {nome}: Média de {formatar_moeda(desc_medio)} por venda")

# 8. Origem dos Clientes
print("\n8. 📍 Faturamento por Cidade dos Clientes:")
cursor.execute("""
    SELECT c.cidade, SUM(v.preco_venda), COUNT(v.id)
    FROM vendas v JOIN clientes c ON v.cliente_id = c.id
    GROUP BY c.cidade ORDER BY SUM(v.preco_venda) DESC
""")
for cid, fat, qtd in cursor.fetchall():
    print(f"   - {cid}: {formatar_moeda(fat)} ({qtd} vendas)")

# 9. Ranking de Vendedores por Filial
print("\n9. 🚩 Vendedores Destaque em cada Filial:")
cursor.execute("""
    SELECT f.nome, v.nome, SUM(ven.preco_venda)
    FROM vendas ven
    JOIN vendedores v ON ven.vendedor_id = v.id
    JOIN filiais f ON ven.filial_id = f.id
    GROUP BY f.nome, v.nome ORDER BY f.nome, SUM(ven.preco_venda) DESC
""")
for filial, vend, fat in cursor.fetchall():
    print(f"   - [{filial}] {vend}: {formatar_moeda(fat)}")

# 10. Maior Venda
print("\n10. 💎 Venda de Maior Valor Registrada:")
cursor.execute("""
    SELECT v.id, v.preco_venda, c.modelo, cli.nome, vend.nome
    FROM vendas v
    JOIN carros c ON v.carro_id = c.id
    JOIN clientes cli ON v.cliente_id = cli.id
    JOIN vendedores vend ON v.vendedor_id = vend.id
    ORDER BY v.preco_venda DESC LIMIT 1
""")
venda_top = cursor.fetchone()
if venda_top:
    print(f"   - Venda #{venda_top[0]}: {formatar_moeda(venda_top[1])} | Carro: {venda_top[2]} | Cliente: {venda_top[3]} | Vendedor: {venda_top[4]}")

conn.close()
print("\n" + "=" * 65)
