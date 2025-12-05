import requests
import pandas as pd
from pathlib import Path

# --- DESAFIO: INTEGRAÇÃO CRM (REQUESTS + PANDAS) ---
# Objetivo: Consultar uma lista de usuários na API e gerar um Excel para o Marketing.
# Requisitos: Tratamento de erro para usuários inexistentes.

# 1. Configuração Inicial
# Lista de IDs que precisamos enriquecer com dados da API.
# Note que o ID 150 não existe propositalmente para testarmos o erro.
ids_usuarios = [1, 3, 5, 150]

# Onde vamos salvar o relatório final?
# Usando pathlib para garantir que funcione em Windows/Mac/Linux
arquivo_saida = Path.cwd() / "relatorio_leads.xlsx"

# Lista vazia para acumularmos os dados processados antes de criar o DataFrame
dados_processados = []

print("--- INICIANDO PROCESSAMENTO DE LEADS ---\n")

# 2. Loop de Processamento
# Para cada ID na nossa lista, vamos fazer uma chamada de API.
for id_usuario in ids_usuarios:
    print(f"Consultando usuário ID: {id_usuario}...", end="")
    
    url = f"https://jsonplaceholder.typicode.com/users/{id_usuario}"
    
    try:
        # Fazendo a requisição GET
        response = requests.get(url)
        
        # AQUI ESTÁ O TRULO (A Regra de Ouro):
        # O .raise_for_status() vai olhar o código HTTP.
        # Se for 200 (OK), não faz nada.
        # Se for 404 (Não Encontrado) ou 500 (Erro Servidor), lança um erro (exceção).
        response.raise_for_status()
        
        # --- SUCESSO ---
        # Se o código chegou aqui, significa que o usuário existe!
        dados_api = response.json()
        
        # Extraindo apenas o que o Marketing pediu
        # O JSON da API user tem campos aninhados (address -> city)
        info_usuario = {
            "ID": id_usuario,
            "Nome": dados_api["name"],
            "Email": dados_api["email"],
            "Cidade": dados_api["address"]["city"],
            "Status": "Ativo" # Campo extra que criamos
        }
        print(" OK!")
        
    except requests.exceptions.HTTPError as e:
        # --- ERRO ---
        # Aconteceu algum erro HTTP (ex: 404 Not Found)
        print(" FALHOU (Não Encontrado)")
        
        # Estratégia de Fallback:
        # Mesmo com erro, queremos registrar esse ID no relatório,
        # mas com valores vazios, para o time saber que procuramos.
        info_usuario = {
            "ID": id_usuario,
            "Nome": "Não Encontrado",
            "Email": "-",
            "Cidade": "-",
            "Status": "Erro na Consulta"
        }
        
    except Exception as e:
        # Captura erros genéricos (ex: sem internet)
        print(f" ERRO CRÍTICO: {e}")
        continue # Pula para o próximo ID

    # Adicionamos o dicionário (seja de sucesso ou erro) na nossa lista principal
    dados_processados.append(info_usuario)

# 3. Geração do Relatório (PANDAS)
print("\n--- GERANDO RELATÓRIO EXCEL ---")

# Transformando a lista de dicionários em uma Tabela (DataFrame)
df = pd.DataFrame(dados_processados)

# Mostrando uma prévia no terminal
print(df)

# Salvando em Excel
try:
    # index=False: Não queremos salvar os números 0, 1, 2, 3... da margem do pandas
    df.to_excel(arquivo_saida, index=False)
    print(f"\n✅ SUCESSO! Relatório salvo em: {arquivo_saida}")
except ModuleNotFoundError:
    print("\n⚠️  AVISO: Biblioteca 'openpyxl' não encontrada.")
    print("Para salvar em Excel, instale com: pip install openpyxl")
    print("Salvando em CSV como alternativa...")
    df.to_csv(arquivo_saida.with_suffix(".csv"), index=False)
except Exception as e:
    print(f"\n❌ Erro ao salvar arquivo: {e}")
