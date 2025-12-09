# 📊 Integrador CRM - Enriquecimento de Leads

Este projeto é uma automação desenvolvida em Python para simular o enriquecimento de dados de leads. O script consome uma API externa para buscar detalhes de usuários com base em uma lista de IDs e gera um relatório consolidado para a equipe de Marketing.

O objetivo principal é demonstrar a integração entre **Consumo de APIs (REST)** e **Engenharia de Dados (Pandas)**, com foco em robustez e tratamento de falhas.

## 🚀 Funcionalidades

- **Consumo de API REST:** Realiza requisições HTTP GET para obter dados detalhados de usuários (simulado via JSONPlaceholder).
- **Tratamento de Erros Robusto (Fail Gracefully):**
    - Identifica IDs inexistentes (Erro 404) e registra como "Não Encontrado" em vez de quebrar a execução.
    - Captura falhas de conexão ou erros de servidor (5xx).
- **Parsing de Dados Aninhados:** Extrai e "achata" dados complexos (JSON aninhado, ex: `address.city`) para um formato tabular.
- **Exportação Flexível:**
    - Gera o relatório final em **Excel (.xlsx)**.
    - Possui um sistema de fallback automático para **CSV** caso a biblioteca de Excel não esteja instalada.

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Requests:** Para comunicação HTTP eficiente e segura.
- **Pandas:** Para manipulação, limpeza e exportação dos dados.
- **OpenPyXL:** Engine para gravação de arquivos Excel.
- **Pathlib:** Gerenciamento de caminhos de arquivos compatível com Windows, Linux e Mac.

## 📂 Estrutura do Projeto

```text
integrador-crm/
├── integracao_crm.py    # Script principal da automação
├── requirements.txt     # Dependências específicas deste projeto
├── README.md            # Documentação do projeto
└── relatorio_leads.xlsx # (Gerado após a execução)

## 📦 Instalação

pip install -r requirements.txt