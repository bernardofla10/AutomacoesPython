import pandas as pd
from pathlib import Path

# --- FUNDAMENTOS DE PANDAS PARA AUTOMAÇÃO ---
# Instalação necessária: pip install pandas openpyxl

# 1. Criação de Dados (Simulando uma extração de dados)
# Em automações, muitas vezes você extrai dados de APIs ou sites e monta uma lista de dicionários.
dados_brutos = [
    {"id": 1, "produto": "Notebook", "valor": 4500.00, "status": "entregue"},
    {"id": 2, "produto": "Mouse", "valor": 150.00, "status": "pendente"},
    {"id": 3, "produto": "Teclado", "valor": 300.00, "status": "entregue"},
    {"id": 4, "produto": "Monitor", "valor": 1200.00, "status": "cancelado"},
]

# Criando o DataFrame (a tabela do Excel dentro do Python)
df = pd.DataFrame(dados_brutos)

print("--- Tabela Original ---")
print(df)

# 2. Exportação de Dados (Salvando relatórios)
# É comum salvar o resultado da automação em Excel ou CSV.
arquivo_csv = Path.cwd() / "relatorio_vendas.csv"
arquivo_excel = Path.cwd() / "relatorio_vendas.xlsx"

# index=False remove a numeração das linhas (0, 1, 2...) do arquivo final
df.to_csv(arquivo_csv, index=False, encoding="utf-8")
# df.to_excel(arquivo_excel, index=False) # Requer biblioteca openpyxl

print(f"\nArquivo salvo em: {arquivo_csv}")

# 3. Leitura de Dados
# Lendo o arquivo que acabamos de criar (ou um que veio de outro lugar)
df_lido = pd.read_csv(arquivo_csv)

# 4. Filtragem de Dados (Lógica de Negócio)
# Cenário: Quero apenas os pedidos 'entregue' com valor acima de 1000.
# A sintaxe é: df[ (condicao1) & (condicao2) ]
filtro = (df_lido["status"] == "entregue") & (df_lido["valor"] > 1000)
pedidos_vip = df_lido[filtro]

print("\n--- Pedidos VIP (Entregues e > 1000) ---")
print(pedidos_vip)

# 5. Iteração (Processando linha a linha)
# Embora o pandas seja otimizado para operações em massa (vetorizadas),
# em automação as vezes precisamos iterar para fazer ações externas (ex: enviar um email para cada linha).

print("\n--- Processando Fila de Pedidos ---")
for index, linha in df_lido.iterrows():
    # Acessando os dados da linha
    produto = linha["produto"]
    status = linha["status"]
    
    if status == "pendente":
        print(f"ALERTA: O produto {produto} ainda está pendente. Enviando notificação...")
    elif status == "cancelado":
        print(f"Info: O produto {produto} foi cancelado. Atualizar estoque.")
    else:
        print(f"OK: {produto} processado.")

# 6. Modificação de Dados
# Adicionando uma coluna nova calculada (ex: imposto de 10%)
df_lido["imposto"] = df_lido["valor"] * 0.10

print("\n--- Tabela com Impostos ---")
print(df_lido[["produto", "valor", "imposto"]])

# 7. Limpeza e Datas (O Mundo Real)

# Dados sujos comuns em automação
dados_sujos = [
    {"data": "2024-01-15", "valor_texto": "R$ 1.000,00"},
    {"data": "2024-01-20", "valor_texto": "R$ 500,50"},
    {"data": "invalid_date", "valor_texto": "R$ 0,00"} # Erro proposital
]
df_sujo = pd.DataFrame(dados_sujos)

# Converter coluna de texto para número real (Float)
# O replace troca 'R$ ' por nada e ',' por '.'
df_sujo["valor_real"] = df_sujo["valor_texto"].str.replace("R$ ", "").str.replace(".", "").str.replace(",", ".").astype(float)

# Converter texto para Data (Datetime)
# errors='coerce' transforma erros em NaT (Not a Time) em vez de travar o script
df_sujo["data_formatada"] = pd.to_datetime(df_sujo["data"], errors="coerce")

print("\n--- Tabela Sujos ---")
print(df_sujo)
print(f"Tipos de dados:\n{df_sujo.dtypes}")

# Filtrar apenas onde a data é válida
df_limpo = df_sujo.dropna(subset=["data_formatada"])

print("\n--- Tabela Limpa ---")
print(df_limpo)
print(f"Tipos de dados:\n{df_limpo.dtypes}")


