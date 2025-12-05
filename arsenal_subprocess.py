import subprocess

# --- FUNDAMENTOS DE SUBPROCESS PARA AUTOMAÇÃO ---
# O módulo subprocess permite rodar comandos do sistema operacional (CMD/Terminal)
# diretamente pelo Python. É útil para chamar outros scripts, executáveis ou comandos do sistema.

print("--- 1. Execução Simples ---")
# subprocess.run: A forma mais moderna e recomendada de rodar comandos.
# args: Lista com o comando e seus argumentos.
# shell=True: Necessário no Windows para alguns comandos internos (como 'dir', 'echo'),
# mas evite usar se possível por segurança. Para executáveis (.exe), não precisa.

# Exemplo: Rodando um 'echo' (imprimir no terminal)
# No Windows, 'echo' é um comando do shell, então shell=True ajuda.
resultado = subprocess.run(["echo", "Olá do subprocess!"], shell=True)
print(f"Código de retorno: {resultado.returncode}") # 0 significa sucesso

print("\n--- 2. Capturando a Saída (Output) ---")
# Muitas vezes queremos ler o que o comando respondeu.
# capture_output=True: Captura stdout (saída padrão) e stderr (erros).
# text=True: Já decodifica os bytes para string (senão viria b'texto').

# Exemplo: Verificando a versão do python instalada
cmd_versao = ["python", "--version"]
resultado_captura = subprocess.run(cmd_versao, capture_output=True, text=True)

print(f"Comando rodou com sucesso? {resultado_captura.returncode == 0}")
print(f"Saída capturada: {resultado_captura.stdout.strip()}")

print("\n--- 3. Tratamento de Erros ---")
# check=True: Faz o Python lançar um erro (CalledProcessError) se o comando falhar (retorno != 0).
# Isso é vital para automações: se um passo falha, você quer saber e parar/tratar.

comando_invalido = ["python", "--comando-que-nao-existe"]

try:
    print("Tentando rodar comando inválido...")
    subprocess.run(comando_invalido, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"ERRO CAPTURADO: O comando falhou com código {e.returncode}")
    print(f"Detalhe do erro (stderr): {e.stderr.strip()}")
except FileNotFoundError:
    # Acontece se o executável principal não for encontrado (ex: tentar rodar 'programa_x' e ele não existir)
    print("ERRO: O executável não foi encontrado no sistema.")

print("\n--- 4. Timeout (Evitando travamentos) ---")
# timeout=X: Mata o processo se ele demorar mais que X segundos.
try:
    # 'ping -n 5' tenta pingar 5 vezes (demora ~5s). Timeout de 2s vai falhar.
    subprocess.run(["ping", "-n", "5", "8.8.8.8"], capture_output=True, timeout=2)
except subprocess.TimeoutExpired:
    print("ALERTA: O comando demorou muito e foi cancelado.")

print("\n--- 5. Controlando o Ambiente de Execução ---")

# Muitas vezes você precisa rodar um comando dentro de uma pasta específica.
# ex: rodar um git pull dentro da pasta do repositório
# Cenário: Quero rodar um comando dentro da pasta 'dados' sem mudar o meu script de lugar
pasta_alvo = Path.cwd() / "dados"
pasta_alvo.mkdir(exist_ok=True)

# Como injetar uma senha ou token no subprocesso sem salvar no arquivo ou no sistema global? 
# Você passa um dicionário de ambiente customizado, um ambiente virtual.
# Cenário: O programa que vou chamar precisa de uma SENHA específica
# Copiamos as variáveis do sistema atual e adicionamos a nossa
meu_ambiente = os.environ.copy()
meu_ambiente["SENHA_BANCO"] = "123456"

# cwd=... : Muda o diretório SÓ para este comando
# env=... : Passa as variáveis de ambiente SÓ para este comando
cmd = ["python", "-c", "import os; print(f'Estou em: {os.getcwd()}'); print(f'Senha: {os.environ.get('SENHA_BANCO')}')"]

subprocess.run(cmd, cwd=pasta_alvo, env=meu_ambiente, text=True)
