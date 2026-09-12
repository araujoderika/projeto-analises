# 🚗 Premium Motors — Análise de Vendas Multi-Filial em SQL

Projeto de banco de dados relacional e análise de vendas para uma
concessionária fictícia com 3 filiais, simulando um cenário real de
**Business Intelligence** no varejo automotivo.

## 🎯 Contexto e Problema de Negócio

A diretoria comercial da Premium Motors precisa de respostas rápidas
para decisões do dia a dia:

- A empresa está performando bem? Quanto faturou?
- Quais vendedores e filiais são os melhores — e quais precisam de apoio?
- Existe estoque parado consumindo capital sem retorno?
- Os descontos concedidos estão sob controle?
- Em quais meses e regiões vale a pena investir mais em marketing?

Este projeto modela um banco de dados relacional para uma concessionária
com múltiplas filiais e escreve consultas SQL que respondem a cada uma
dessas perguntas com dados.

## 🔎 Perguntas de negócio respondidas (com SQL)

| # | Pergunta de negócio |
|---|---|
| 1 | Qual o faturamento total e o ticket médio? |
| 2 | Quem são os top 3 vendedores por faturamento? |
| 3 | Qual filial fatura mais / vende mais unidades? |
| 4 | Qual categoria de carro gera mais receita? |
| 5 | Quais carros estão parados em estoque (capital empatado)? |
| 6 | Como o faturamento evoluiu mês a mês? |
| 7 | Qual vendedor concede mais desconto em média? |
| 8 | De quais cidades vêm os clientes que mais compram? |
| 9 | Ranking de vendedores agrupado por filial? |
| 10 | Qual foi a venda de maior valor do período? |

## 📊 Principais Insights (a partir dos dados simulados)

> Dados sintéticos gerados para fins de portfólio — 130 vendas ao longo de 2025.

- **Faturamento total simulado:** R$ 27,3 milhões, com ticket médio de ~R$ 210 mil por venda
- **Categoria "Esportivo"** foi a que mais gerou receita (R$ 12,6 mi em apenas 17 unidades) — ticket alto compensa baixo volume
- A filial **Barueri** liderou em faturamento, mesmo com menos vendas que Campinas — indício de mix de produto mais premium
- Fevereiro/2025 foi o mês de maior faturamento — possível sazonalidade a investigar
- Foram identificadas unidades de "Hatch" com maior concentração parada em estoque, sinalizando possível necessidade de ação promocional

## 💰 Relatório com valores formatados como moeda

O SQL puro não formata moeda no padrão brasileiro (R$ 1.234.567,89) —
essa responsabilidade fica pra camada de apresentação. Por isso, além
das queries, o projeto inclui [`relatorio_negocio.py`](relatorio_negocio.py),
que roda as principais análises e imprime os números já formatados:

```bash
python3 relatorio_negocio.py
```

Saída de exemplo:

```
=======================================================
RELATÓRIO DE NEGÓCIO — PREMIUM MOTORS
=======================================================

📊 Total de vendas no período: 12
💰 Faturamento total: R$ 20.377.619,62
🎫 Ticket médio: R$ 210.597,07

🏆 Top 3 vendedores por faturamento:
   - Patrícia Gomes: R$ 5.287.757,02
   - Camila Rocha: R$ 3.865.063,01
   - Lucas Martins: R$ 3.726.450,87

🏢 Faturamento por filial:
   - Premium Motors - Barueri: R$ 13.287.324,41 (5 unidades)
   - Premium Motors - Campinas: R$ 10.468.217,84 (4 unidades)
   - Premium Motors - Osasco: R$ 3.622.077,37 (3 unidades)
```

## 🛠️ Como rodar este projeto

Requer apenas o [SQLite](https://www.sqlite.org/) (ou qualquer SGBD compatível
com pequenas adaptações de sintaxe).

```bash
sqlite3 premium_motors.db < sql/01_schema.sql
sqlite3 premium_motors.db < sql/02_dados.sql
sqlite3 premium_motors.db < sql/03_perguntas_de_negocio.sql
```

Ou, usando o DB Browser for SQLite: crie um banco novo, abra o "Execute SQL"
e rode os três arquivos na ordem (schema → dados → perguntas).

## 📁 Estrutura do repositório

```
premium-motors-analise-vendas/
├── sql/
│   ├── 01_schema.sql               → criação das tabelas
│   ├── 02_dados.sql                → carga de dados de exemplo
│   └── 03_perguntas_de_negocio.sql → as 10 análises de negócio
├── gerar_dados.py                  → script usado para gerar os dados sintéticos
├── relatorio_negocio.py            → roda as análises e formata os valores em R$
└── README.md
```

## 🚀 Próximos passos

- Conectar este banco a uma ferramenta de BI (Power BI / Looker Studio) para
  um dashboard visual
- Adicionar análise de sazonalidade e projeção de vendas futuras
- Expandir o modelo para incluir pós-venda e satisfação do cliente

---

**Tecnologias:** SQL (SQLite) · Python (geração de dados) · Modelagem relacional

**Autora:** Érika Araujo — [LinkedIn](https://www.linkedin.com/in/erikadaraujo/)
