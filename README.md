# 🚗 Premium Motors — Análise de Banco de Dados & Relatório de Negócio

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Projeto de modelagem de banco de dados relacional e automação de relatório gerencial para a concessionária de luxo **Premium Motors**. 

O sistema integra a criação de estrutura de dados (DDL), carga de dados (DML) e execução automatizada via Python para responder a **10 perguntas estratégicas de negócio**.

---

## 📌 Funcionalidades Principais

- 🗄️ **Modelagem Relacional (SQL):** Criação de tabelas relacionais (`carros`, `clientes`, `vendedores`, `filiais`, `vendas`).
- ⚡ **Automação via Python:** Leitura automatizada dos scripts `.sql` e execução direta no banco **SQLite**.
- 📊 **10 Análises Estratégicas:** Consultas complexas usando `JOIN`, `GROUP BY`, `SUM`, `AVG`, `LEFT JOIN` e funções de agregação.
- 💵 **Formatação de Valores:** Exibição amigável dos resultados financeiros em moeda brasileira (`R$`).

---

## 📊 As 10 Análises de Negócio Incluídas
1.Faturamento Total, Ticket Médio e Volume de Vendas

2.Top 3 Vendedores por Faturamento

3.Desempenho por Filial (Barueri, Campinas, Osasco)

4.Receita por Categoria de Veículo (Esportivo, Hatch, Sedan, etc.)

5.Estoque Parado (Modelos sem vendas registradas)

6.Evolução Mensal do Faturamento

7.Média de Desconto Concedido por Vendedor

8.Faturamento por Cidade de Origem dos Clientes

9.Ranking dos Vendedores por Filial

10.Identificação da Venda de Maior Valor (Ticket Máximo)

## 🚀 Como Executar o Projeto
Pré-requisitos
Python 3.8+ instalado.

## Passo a Passo
Clone o repositório:

Bash
git clone [https://github.com/seu-usuario/premium-motors.git](https://github.com/seu-usuario/premium-motors.git)
cd premium-motors

Execute o script principal:

Bash
python relatorio.negocio.py
## 📸 Exemplo de Execução
Ao rodar o script relatorio.negocio.py, a saída formatada no terminal exibe o relatório gerencial completo:
<img width="1873" height="956" alt="Captura de tela 2026-09-12 164657" src="https://github.com/user-attachments/assets/a9a76250-3519-4858-9335-31cbe08c6fd0" />



## 🛠️ Tecnologias Utilizadas
Python: Automação e formatação de relatório.

SQLite3: Banco de dados relacional.

SQL (DDL & DML): Modelagem e consultas.

## ✒️ Autor
Desenvolvido por Érika Araujo 👋

GitHub: @araujoderika
LinkedIn: https://www.linkedin.com/in/erikadaraujo/
