import random
import sqlite3

random.seed(42)

filiais = [
    (1, "Premium Motors - Osasco", "Osasco/SP"),
    (2, "Premium Motors - Barueri", "Barueri/SP"),
    (3, "Premium Motors - Campinas", "Campinas/SP"),
]

vendedores = [
    (1, "Marcos Ribeiro", 1),
    (2, "Fernanda Costa", 1),
    (3, "João Pedro Alves", 2),
    (4, "Camila Rocha", 2),
    (5, "Rafael Nunes", 3),
    (6, "Bianca Ferreira", 3),
    (7, "Lucas Martins", 1),
    (8, "Patrícia Gomes", 2),
]

modelos = [
    ("Toyota", "Corolla", "Sedan", 145000),
    ("Chevrolet", "Onix", "Hatch", 82000),
    ("Ford", "Mustang", "Esportivo", 350000),
    ("Volkswagen", "Gol", "Hatch", 65000),
    ("Honda", "Civic", "Sedan", 155000),
    ("Jeep", "Compass", "SUV", 180000),
    ("Fiat", "Mobi", "Hatch", 58000),
    ("BMW", "X1", "SUV", 280000),
    ("Hyundai", "HB20", "Hatch", 75000),
    ("Porsche", "911", "Esportivo", 900000),
    ("Toyota", "Hilux", "Picape", 260000),
    ("Volkswagen", "T-Cross", "SUV", 145000),
    ("Chevrolet", "Tracker", "SUV", 135000),
    ("Renault", "Kwid", "Hatch", 62000),
    ("Nissan", "Kicks", "SUV", 128000),
]

cidades_clientes = ["Osasco", "Barueri", "Campinas", "São Paulo", "Jundiaí", "Cotia"]

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.executescript("""
CREATE TABLE filiais (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    localizacao TEXT
);
CREATE TABLE vendedores (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    id_filial INTEGER,
    FOREIGN KEY (id_filial) REFERENCES filiais(id)
);
CREATE TABLE carros (
    id INTEGER PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    categoria TEXT,
    preco_tabela REAL,
    id_filial INTEGER,
    em_estoque INTEGER,
    FOREIGN KEY (id_filial) REFERENCES filiais(id)
);
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    cidade TEXT
);
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY,
    id_carro INTEGER,
    id_cliente INTEGER,
    id_vendedor INTEGER,
    data_venda TEXT,
    preco_final REAL,
    FOREIGN KEY (id_carro) REFERENCES carros(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_vendedor) REFERENCES vendedores(id)
);
""")

cur.executemany("INSERT INTO filiais VALUES (?,?,?)", filiais)
cur.executemany("INSERT INTO vendedores VALUES (?,?,?)", vendedores)

# Gerar 60 carros no estoque, distribuídos entre filiais
carros = []
carro_id = 1
for _ in range(60):
    marca, modelo, categoria, preco_base = random.choice(modelos)
    preco_tabela = round(preco_base * random.uniform(0.95, 1.08), 2)
    id_filial = random.choice([1, 2, 3])
    carros.append((carro_id, marca, modelo, categoria, preco_tabela, id_filial, 1))
    carro_id += 1
cur.executemany("INSERT INTO carros VALUES (?,?,?,?,?,?,?)", carros)

# Gerar 40 clientes
clientes = []
nomes = ["Ana", "Bruno", "Carla", "Diego", "Erika", "Felipe", "Gabriela", "Henrique",
         "Isabela", "João", "Karina", "Leonardo", "Mariana", "Natália", "Otávio",
         "Paula", "Rodrigo", "Sabrina", "Tiago", "Vanessa"]
sobrenomes = ["Silva", "Souza", "Lima", "Oliveira", "Pereira", "Santos", "Costa", "Rocha"]
for i in range(1, 41):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    cidade = random.choice(cidades_clientes)
    clientes.append((i, nome, cidade))
cur.executemany("INSERT INTO clientes VALUES (?,?,?)", clientes)

# Gerar 130 vendas ao longo de 12 meses (2025), algumas com desconto
meses = [f"2025-{m:02d}" for m in range(1, 13)]
vendas = []
for i in range(1, 131):
    id_carro = random.randint(1, 60)
    id_cliente = random.randint(1, 40)
    id_vendedor = random.randint(1, 8)
    mes = random.choice(meses)
    dia = random.randint(1, 28)
    data_venda = f"{mes}-{dia:02d}"
    preco_tabela = [c[4] for c in carros if c[0] == id_carro][0]
    desconto = random.uniform(0, 0.08)
    preco_final = round(preco_tabela * (1 - desconto), 2)
    vendas.append((i, id_carro, id_cliente, id_vendedor, data_venda, preco_final))
cur.executemany("INSERT INTO vendas VALUES (?,?,?,?,?,?)", vendas)

conn.commit()

# Marcar carros vendidos como fora de estoque
cur.execute("""
    UPDATE carros SET em_estoque = 0
    WHERE id IN (SELECT id_carro FROM vendas)
""")
conn.commit()

# Exportar tudo como INSERTs pra um arquivo .sql
def export_inserts(table, rows, cols):
    lines = []
    for row in rows:
        vals = []
        for v in row:
            if isinstance(v, str):
                vals.append("'" + v.replace("'", "''") + "'")
            else:
                vals.append(str(v))
        lines.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(vals)});")
    return "\n".join(lines)

with open("dados_inserts.sql", "w") as f:
    f.write("-- Filiais\n")
    f.write(export_inserts("filiais", filiais, ["id", "nome", "localizacao"]) + "\n\n")
    f.write("-- Vendedores\n")
    f.write(export_inserts("vendedores", vendedores, ["id", "nome", "id_filial"]) + "\n\n")
    f.write("-- Carros (estoque)\n")
    carros_atualizados = cur.execute("SELECT * FROM carros").fetchall()
    f.write(export_inserts("carros", carros_atualizados,
             ["id", "marca", "modelo", "categoria", "preco_tabela", "id_filial", "em_estoque"]) + "\n\n")
    f.write("-- Clientes\n")
    f.write(export_inserts("clientes", clientes, ["id", "nome", "cidade"]) + "\n\n")
    f.write("-- Vendas\n")
    f.write(export_inserts("vendas", vendas,
             ["id", "id_carro", "id_cliente", "id_vendedor", "data_venda", "preco_final"]) + "\n")

print("Arquivo dados_inserts.sql gerado com sucesso!")

# ---- Calcular insights reais pra usar no README ----
print("\n--- INSIGHTS REAIS ---")

faturamento_total = cur.execute("SELECT SUM(preco_final) FROM vendas").fetchone()[0]
print("Faturamento total:", round(faturamento_total, 2))

ticket_medio = cur.execute("SELECT AVG(preco_final) FROM vendas").fetchone()[0]
print("Ticket médio:", round(ticket_medio, 2))

top_vendedor = cur.execute("""
    SELECT v.nome, SUM(vd.preco_final) as total
    FROM vendas vd JOIN vendedores v ON vd.id_vendedor = v.id
    GROUP BY v.nome ORDER BY total DESC LIMIT 3
""").fetchall()
print("Top 3 vendedores:", top_vendedor)

top_filial = cur.execute("""
    SELECT f.nome, SUM(vd.preco_final) as total, COUNT(*) as qtd
    FROM vendas vd
    JOIN carros c ON vd.id_carro = c.id
    JOIN filiais f ON c.id_filial = f.id
    GROUP BY f.nome ORDER BY total DESC
""").fetchall()
print("Faturamento por filial:", top_filial)

top_categoria = cur.execute("""
    SELECT c.categoria, COUNT(*) as qtd, SUM(vd.preco_final) as total
    FROM vendas vd JOIN carros c ON vd.id_carro = c.id
    GROUP BY c.categoria ORDER BY total DESC
""").fetchall()
print("Vendas por categoria:", top_categoria)

estoque_parado = cur.execute("""
    SELECT categoria, COUNT(*) FROM carros WHERE em_estoque = 1 GROUP BY categoria ORDER BY 2 DESC
""").fetchall()
print("Estoque parado por categoria:", estoque_parado)

melhor_mes = cur.execute("""
    SELECT data_venda_mes, SUM(preco_final) as total FROM (
        SELECT substr(data_venda,1,7) as data_venda_mes, preco_final FROM vendas
    ) GROUP BY data_venda_mes ORDER BY total DESC LIMIT 1
""").fetchone()
print("Melhor mês:", melhor_mes)

total_vendas = cur.execute("SELECT COUNT(*) FROM vendas").fetchone()[0]
print("Total de vendas no período:", total_vendas)

conn.close()
