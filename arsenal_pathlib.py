from pathlib import Path

# --- FUNDAMENTOS DE PATHLIB PARA AUTOMAÇÃO ---

# 1. Identificar caminhos importantes
# Path.cwd(): Retorna o diretório onde o script está sendo executado (Current Working Directory)
diretorio_atual = Path.cwd()
print(f"1. Diretório atual: {diretorio_atual}")

# Path.home(): Retorna o diretório do usuário (ex: C:\Users\SeuUsuario)
diretorio_usuario = Path.home()
print(f"2. Diretório do usuário: {diretorio_usuario}")

# 2. Construção de caminhos (Path Joining)
# A barra '/' é sobrecarregada no pathlib para funcionar como união de caminhos,
# independente do sistema operacional (Windows usa \, Linux/Mac usa /).
# Isso torna o código portável e evita erros de string.
pasta_dados = diretorio_atual / "dados"
pasta_relatorios = pasta_dados / "relatorios"
arquivo_log = pasta_dados / "logs" / "execucao.log"

print(f"3. Caminho construído: {arquivo_log}")

# 3. Gerenciamento de Diretórios
# mkdir(): Cria o diretório.
# parents=True: Cria todas as pastas pai necessárias (ex: cria 'dados', depois 'logs').
# exist_ok=True: Não gera erro se a pasta já existir (essencial para automações recorrentes).
pasta_relatorios.mkdir(parents=True, exist_ok=True)
arquivo_log.parent.mkdir(parents=True, exist_ok=True) # .parent pega a pasta do arquivo

print("4. Pastas criadas (ou verificadas) com sucesso.")

# 4. Informações e Manipulação de Arquivos
# Vamos criar um arquivo fictício para testar
arquivo_exemplo = pasta_relatorios / "relatorio_janeiro_2024.pdf"
# touch() cria um arquivo vazio (similar ao comando touch do Linux), útil para testes
# No Windows, precisamos garantir que o arquivo exista para ler metadados, então vamos escrever algo vazio.
if not arquivo_exemplo.exists():
    arquivo_exemplo.write_text("") 

# Propriedades úteis do objeto Path:
print(f"\n--- Analisando: {arquivo_exemplo.name} ---")
print(f"Nome completo: {arquivo_exemplo.name}")      # relatorio_janeiro_2024.pdf
print(f"Nome sem extensão (stem): {arquivo_exemplo.stem}") # relatorio_janeiro_2024
print(f"Extensão (suffix): {arquivo_exemplo.suffix}")      # .pdf
print(f"Pasta pai (parent): {arquivo_exemplo.parent}")     # ...\dados\relatorios

# 5. Verificações (Checagens de existência)
if arquivo_exemplo.exists():
    print("-> O arquivo existe.")
    
    if arquivo_exemplo.is_file():
        print("-> É um arquivo.")
    
    if arquivo_exemplo.is_dir():
        print("-> É uma pasta.")
else:
    print("-> Arquivo não encontrado.")

# 6. Listagem de Arquivos (Globbing)
# glob('*'): Lista tudo na pasta.
# glob('*.pdf'): Lista apenas PDFs.
# rglob('*.txt'): Lista recursivamente (entra em subpastas) procurando txt.

print("\n--- Listando arquivos na pasta de relatórios ---")
# Vamos criar mais um arquivo para ilustrar
(pasta_relatorios / "relatorio_fevereiro.pdf").write_text("")

for arquivo in pasta_relatorios.glob("*.pdf"):
    print(f"Encontrado: {arquivo.name}")

# 7. Leitura e Escrita Rápida (para arquivos de texto pequenos)
arquivo_config = diretorio_atual / "config.txt"

# Escrevendo texto
texto_config = "status=ativo\nversao=1.0"
arquivo_config.write_text(texto_config, encoding="utf-8")
print(f"\nArquivo de config criado em: {arquivo_config}")

# Lendo texto
conteudo = arquivo_config.read_text(encoding="utf-8")
print(f"Conteúdo lido:\n{conteudo}")

# Limpeza (Opcional - para não deixar lixo no seu computador)
# arquivo_config.unlink() # Deleta arquivo
# pasta_relatorios.rmdir() # Deleta pasta (só se estiver vazia)

# Quando você passa um caminho de arquivo para um programa externo (via subprocess) 
# ou para uma API, eles muitas vezes não entendem caminhos relativos (ex: ../dados). 
# Você precisa transformar o caminho em absoluto.

# 8. Caminhos Absolutos (Crucial para integração com Subprocess)
# Transforma 'dados/relatorio.pdf' em 'C:\Users\Voce\Projeto\dados\relatorio.pdf'
caminho_relativo = Path("dados/relatorios")
caminho_absoluto = caminho_relativo.resolve()
print(f"Caminho absoluto: {caminho_absoluto}")

# Em automação, é padrão mover um arquivo da pasta "Entrada" para a pasta "Processados"
# após o script rodar. O método .rename() faz isso.

# 9. Movendo arquivos (Fluxo de Processamento)
arquivo_entrada = Path("inbox/pedido_123.txt")
pasta_processados = Path("processed")

# Se o arquivo existe, movemos ele
if arquivo_entrada.exists():
    pasta_processados.mkdir(exist_ok=True)
    
    # .rename() move o arquivo. O replace garante que sobrescreve se já existir lá.
    destino = pasta_processados / arquivo_entrada.name
    arquivo_entrada.replace(destino)
    print(f"Arquivo movido para: {destino}")