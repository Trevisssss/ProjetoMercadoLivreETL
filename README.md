# Projeto ETL - Coleta de Dados do Mercado Livre

## Descrição

Este projeto tem como objetivo realizar a coleta de dados do site do Mercado Livre, processá-los e armazená-los em um banco de dados para análises posteriores. A aplicação utiliza técnicas de ETL (Extract, Transform, Load) para extrair informações relevantes, transformá-las em um formato estruturado e carregá-las em um banco de dados relacional.

## Funcionalidades

- **Extração de Dados**: Coleta de informações de produtos, como título, preço, descrição, vendedor, entre outros.
- **Transformação de Dados**: Limpeza e padronização dos dados coletados para garantir consistência e qualidade.
- **Armazenamento**: Inserção dos dados processados em um banco de dados para consultas e análises futuras.

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Bibliotecas**: 
    - `scrapy` para web scraping
    - `pandas` para manipulação de dados
- **Banco de Dados**: MySQL ou PostgreSQL
- **Ferramentas de ETL**: Scripts customizados em Python

## Estrutura do Projeto

```
ProjetoETL/
│
├── src/
│   ├── extract.py       # Script para extração de dados
│   ├── transform.py     # Script para transformação de dados
│   └── load.py          # Script para carregamento de dados
│
├── data/
│   └── raw/             # Dados brutos extraídos
│
├── docs/
│   └── especificacoes.md # Documentação técnica
│
├── tests/
│   └── test_etl.py      # Testes automatizados
│
└── README.md            # Documentação do projeto