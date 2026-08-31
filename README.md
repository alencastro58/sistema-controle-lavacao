# Sistema de Controle de Lavação

Sistema web para gerenciamento de uma lavação de veículos.

## Objetivo

O sistema tem como finalidade controlar o atendimento de veículos, clientes, serviços prestados, preços e Ordens de Serviço (OS), incluindo posteriormente um programa de fidelidade baseado em pontuação.

## Escopo inicial

O sistema deverá contemplar:

- cadastro de clientes;
- cadastro de veículos;
- cadastro de categorias de veículos;
- cadastro de serviços;
- configuração de preços dos serviços;
- criação e gerenciamento de Ordens de Serviço;
- aplicação de descontos;
- controle dos estados da OS;
- histórico das operações;
- programa de fidelidade e pontuação.

## Categorias de veículos

As categorias inicialmente previstas são:

- Pequeno;
- Médio;
- Grande;
- Padrão/Comum;
- Moto.

## Serviços

Exemplos inicialmente previstos:

- Lavação completa;
- Impermeabilização de bancos;
- Lavação de motor;
- Polimento;
- Polimento espelhado;
- Polimento de rodas.

O preço de um serviço poderá depender da categoria do veículo ou possuir valor único, conforme a regra definida para o serviço.

## Ordens de Serviço

Uma Ordem de Serviço deverá estar vinculada a um veículo e poderá conter vários serviços.

A OS deverá possuir, entre outras informações:

- número;
- data/agendamento;
- veículo;
- serviços;
- valor total;
- desconto, quando aplicável;
- situação.

Os estados previstos são:

- ABERTA;
- FECHADA;
- CANCELADA.

Uma OS ABERTA poderá ser alterada.

Uma OS FECHADA ou CANCELADA não deverá permitir movimentações operacionais posteriores, preservando seu histórico.

## Valores dos serviços

O preço cadastrado para um serviço será utilizado como referência.

O valor efetivamente praticado em uma OS deverá ser registrado no respectivo item da OS, permitindo que uma cobrança excepcional não altere o preço cadastrado do serviço.

## Programa de fidelidade

O sistema poderá atribuir pontos ao cliente em função dos serviços realizados.

A pontuação deverá possuir histórico das movimentações e ser exclusiva e intransferível para utilização pelo respectivo cliente.

As regras de geração, utilização, resgate e eventual expiração dos pontos serão especificadas antes da implementação desse módulo.

## Tecnologias

### Backend

- Python
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript

### Banco de dados

- PostgreSQL

### Persistência e migrações

- SQLAlchemy
- Alembic

### Desenvolvimento e controle de versão

- Visual Studio Code
- Git
- GitHub

### Hospedagem

- Render

## Arquitetura

A aplicação será desenvolvida com separação de responsabilidades entre:

- apresentação;
- rotas;
- regras de negócio;
- persistência;
- modelos;
- infraestrutura.

A arquitetura deverá priorizar:

- baixo acoplamento;
- alta coesão;
- facilidade de manutenção;
- testabilidade;
- segurança;
- possibilidade de expansão.

## Ambiente local

Diretório:

`D:\Aplicativos\sistema-controle-lavacao`

Ambiente virtual Python:

`.venv`

Python atualmente instalado:

`3.14.5`

## Repositório

GitHub:

`alencastro58/sistema-controle-lavacao`

Branch principal:

`main`

## Implantação

A aplicação será preparada para execução no Render.

O ambiente de produção deverá utilizar PostgreSQL e variáveis de ambiente para configurações e credenciais.

O ambiente virtual `.venv` e informações sensíveis não deverão ser versionados.

## Segurança e proteção de dados

O sistema deverá ser desenvolvido considerando requisitos de segurança da aplicação e, quando houver tratamento de dados pessoais, os requisitos aplicáveis da Lei nº 13.709/2018 — Lei Geral de Proteção de Dados Pessoais (LGPD).

Credenciais, chaves e outros segredos não deverão ser armazenados no código-fonte ou no repositório.

## Testes

O projeto possuirá uma estrutura específica para testes automatizados.

As regras críticas de negócio deverão ser testadas antes da disponibilização da funcionalidade correspondente.

## Estrutura inicial

```text
sistema-controle-lavacao/
│
├── .git/
├── .venv/
├── app/
├── tests/
├── .gitignore
└── README.md