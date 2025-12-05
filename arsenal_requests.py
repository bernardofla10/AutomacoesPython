# Instalação necessária:
# pip install requests python-dotenv

import os
import requests
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL ---
# Carrega variáveis de ambiente do arquivo .env (se existir)
# Isso é vital para não deixar senhas/tokens hardcoded no código (Segurança!)
load_dotenv()

# Simulando o carregamento de um token (em produção, viria do .env)
API_TOKEN = os.getenv("API_TOKEN", "token_ficticio_12345")
BASE_URL = "https://jsonplaceholder.typicode.com"

print("--- INICIANDO ARSENAL REQUESTS ---\n")

# --- 2. REQUISIÇÃO GET SIMPLES ---
# Objetivo: Buscar dados de um usuário específico.
print(">>> 2. GET: Buscando usuário...")

url_usuario = f"{BASE_URL}/users/1"
response = requests.get(url_usuario)

# Exibindo o Status Code (200 = OK, 404 = Não encontrado, 500 = Erro no servidor)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    # Convertendo a resposta (que vem como texto) para um dicionário Python (JSON)
    dados_usuario = response.json()
    print(f"Nome do Usuário: {dados_usuario['name']}")
    print(f"Email: {dados_usuario['email']}")
else:
    print("Erro ao buscar usuário.")

print("-" * 30)

# --- 3. REQUISIÇÃO POST (ENVIANDO DADOS) ---
# Objetivo: Criar um novo post no sistema.
print("\n>>> 3. POST: Enviando dados...")

url_posts = f"{BASE_URL}/posts"

# Payload: O dicionário com os dados que queremos enviar.
novo_post = {
    "title": "Aprendendo Automação com Python",
    "body": "Requests é uma biblioteca incrível!",
    "userId": 1
}

# O parâmetro 'json' converte automaticamente o dicionário para o formato JSON correto
# e adiciona o header 'Content-Type: application/json'.
response_post = requests.post(url_posts, json=novo_post)

print(f"Status Code: {response_post.status_code}") # 201 = Created
print("Resposta do Servidor (JSON):")
print(response_post.json()) # A API geralmente retorna o objeto criado com um ID novo

print("-" * 30)

# --- 4. TRATAMENTO DE ERROS ROBUSTO (A REGRA DE OURO) ---
# Objetivo: Garantir que o script não quebre silenciosamente ou de forma feia.
print("\n>>> 4. ERRO: Testando URL inexistente...")

url_erro = f"{BASE_URL}/users/999999" # Usuário que não existe

try:
    response_erro = requests.get(url_erro)
    
    # Esta é a linha mágica!
    # Se o status for 4xx ou 5xx, ela lança uma exceção (HTTPError).
    # Se for 200 (OK), ela não faz nada e o código segue.
    response_erro.raise_for_status()
    
    print("Sucesso! (Isso não deve aparecer neste exemplo)")

except requests.exceptions.HTTPError as e:
    # Captura erros de protocolo HTTP (404, 500, 403...)
    print(f"ERRO HTTP CAPTURADO: {e}")
    # Dica: Você pode acessar response_erro.status_code aqui também se precisar
    
except requests.exceptions.ConnectionError:
    # Captura erros de conexão (sem internet, DNS falhou...)
    print("ERRO DE CONEXÃO: Verifique sua internet.")
    
except requests.exceptions.Timeout:
    # Captura se o servidor demorar demais para responder
    print("ERRO DE TIMEOUT: O servidor demorou muito.")
    
except Exception as e:
    # Captura qualquer outro erro genérico
    print(f"ERRO DESCONHECIDO: {e}")

print("-" * 30)

# --- 5. AUTENTICAÇÃO E HEADERS ---
# Objetivo: Enviar metadados (como tokens) para acessar áreas restritas.
print("\n>>> 5. AUTH: Usando Headers...")

# Headers são como "etiquetas" na carta que enviamos ao servidor.
# O mais comum é o 'Authorization' para login.
headers_personalizados = {
    "Authorization": f"Bearer {API_TOKEN}",
    "User-Agent": "MeuScriptPython/1.0" # Identifica quem está acessando
}

# Passamos o dicionário no parâmetro 'headers'
# (Nota: jsonplaceholder ignora o token, mas o código é válido para APIs reais)
response_auth = requests.get(f"{BASE_URL}/posts/1", headers=headers_personalizados)

print(f"Status com Auth: {response_auth.status_code}")
print(f"Headers enviados (User-Agent): {response_auth.request.headers['User-Agent']}")

print("-" * 30)

# --- 6. PERFORMANCE COM SESSIONS ---
# Objetivo: Reutilizar a conexão TCP para múltiplas requisições (muito mais rápido).
print("\n>>> 6. SESSION: Otimizando múltiplas chamadas...")

# Context Manager (with): Garante que a sessão seja fechada ao final
with requests.Session() as sessao:
    # Podemos definir headers padrão para TODAS as requisições desta sessão
    sessao.headers.update({"Authorization": f"Bearer {API_TOKEN}"})
    
    # Simulando um loop de requisições
    for i in range(1, 4):
        url = f"{BASE_URL}/posts/{i}"
        print(f"Baixando Post {i}...")
        
        # Note que usamos 'sessao.get' em vez de 'requests.get'
        resp = sessao.get(url)
        
        # Boa prática: sempre checar erros, mesmo em loop
        try:
            resp.raise_for_status()
            titulo = resp.json()['title']
            # Cortando o título só para não poluir o terminal
            print(f"   -> OK: {titulo[:30]}...") 
        except Exception as e:
            print(f"   -> Falha no Post {i}: {e}")

print("\n--- FIM DO ARSENAL ---")
