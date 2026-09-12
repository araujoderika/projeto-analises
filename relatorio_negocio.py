"""
Relatório de Negócio — Premium Motors
Roda as principais análises de vendas e imprime os valores já
formatados como moeda brasileira (R$ 1.234.567,89).

Por quê um script separado pra isso?
SQL é ótimo pra CALCULAR os números certos, mas não é feito pra
FORMATAR exibição (isso muda de cultura pra cultura: BR usa vírgula
decimal, EUA usa ponto). Essa responsabilidade fica pra camada de
apresentação — aqui, o Python.
"""

import sqlite3


def formatar_moeda(valor: float) -> str:
    """Transforma 27377619.62 em 'R$ 27.377.619,62' (padrão brasileiro)."""
    texto = f"{valor:,.2f}"          # formato EUA: 27,377,619.62
    texto = texto.replace(",", "X")  # protege as vírgulas de milhar
    texto = texto.replace(".", ",")  # o ponto decimal vira vírgula
    texto = texto.replace("X", ".")  # o X (antigo milhar) vira ponto
    return f"R$ {texto}"


# Conecta num banco em memória e carrega o schema + dados
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript(open("sql/01_schema.sql").read())
cur.executescript(open("sql/02_dados.sql").read())

print("=" * 55)
print("RELATÓRIO DE NEGÓCIO — PREMIUM MOTORS")
print("=" * 55)

# 1) Faturamento total e ticket médio
total_vendas, faturamento, ticket = cur.execute("""
    SELECT COUNT(*), SUM(preco_final), AVG(preco_final) FROM vendas
""").fetchone()

print(f"\n📊 Total de vendas no período: {total_vendas}")
print(f"💰 Faturamento total: {formatar_moeda(faturamento)}")
print(f"🎫 Ticket médio: {formatar_moeda(ticket)}")

# 2) Top 3 vendedores
print("\n🏆 Top 3 vendedores por faturamento:")
top_vendedores = cur.execute("""
    SELECT v.nome, SUM(vd.preco_final) as total
    FROM vendas vd JOIN vendedores v ON vd.id_vendedor = v.id
    GROUP BY v.nome ORDER BY total DESC LIMIT 3
""").fetchall()
for nome, total in top_vendedores:
    print(f"   - {nome}: {formatar_moeda(total)}")

# 3) Faturamento por filial
print("\n🏢 Faturamento por filial:")
por_filial = cur.execute("""
    SELECT f.nome, SUM(vd.preco_final) as total, COUNT(*) as qtd
    FROM vendas vd
    JOIN carros c ON vd.id_carro = c.id
    JOIN filiais f ON c.id_filial = f.id
    GROUP BY f.nome ORDER BY total DESC
""").fetchall()
for nome, total, qtd in por_filial:
    print(f"   - {nome}: {formatar_moeda(total)} ({qtd} unidades)")

# 4) Faturamento por categoria
print("\n🚘 Faturamento por categoria de carro:")
por_categoria = cur.execute("""
    SELECT c.categoria, SUM(vd.preco_final) as total
    FROM vendas vd JOIN carros c ON vd.id_carro = c.id
    GROUP BY c.categoria ORDER BY total DESC
""").fetchall()
for categoria, total in por_categoria:
    print(f"   - {categoria}: {formatar_moeda(total)}")

# 5) Valor parado em estoque
valor_parado = cur.execute("""
    SELECT SUM(preco_tabela) FROM carros WHERE em_estoque = 1
""").fetchone()[0]
print(f"\n📦 Valor total parado em estoque: {formatar_moeda(valor_parado)}")

print("\n" + "=" * 55)

conn.close()
