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
    - `numpy` para alguns cálculos e outras manipulações
    - `pyodbc` para conexão com o banco de dados
- **Banco de Dados**: SQL Server
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
```

## Desafios do Projeto

Durante o desenvolvimento deste projeto, algumas dificuldades foram encontradas, como:

- **Web Scraping com Scrapy**: Lidar com mudanças na estrutura do site do Mercado Livre e implementar estratégias para evitar bloqueios por parte do servidor. Essas dificuldades ajudaram a entender melhor como funcionam os mecanismos de scraping e a importância de respeitar as políticas de uso de sites. Além de ter que entender como funciona um html de forma com que eu pudesse encontrar os elementos que eram de interesse.

- **Manipulação de Dados com Pandas e Numpy**: Garantir a consistência e a qualidade dos dados exigiu um bom entendimento de manipulação de dados, limpeza e tratamento de valores ausentes ou inconsistentes, pois o banco exige uma forma específica de comunicação e do tipo de dados aceitos. 

- **Conexão com Banco de Dados usando PyODBC**: Configurar a conexão com o banco de dados SQL Server e otimizar a inserção de dados em massa foi um desafio técnico que proporcionou aprendizado sobre integração de sistemas e boas práticas de desempenho.

- **Simulação de um Projeto Real**: A integração de diferentes etapas do processo ETL, desde a extração até o carregamento, simulou um fluxo de trabalho real, permitindo uma visão prática de como projetos de dados são estruturados e executados.
