import os

# Criação da estrutura de diretórios para o projeto
# Ao iniciar um novo projeto em Python pode-se usar este script para criar a estrutura básica de diretórios e arquivos
# Lista de caminhos de diretórios aninhados a serem criados
# Use barras normais (/) ou os.path.join para compatibilidade entre sistemas operacionais
lista_caminhos = [
    "src/api/",
    "src/models/",
    "src/data/",
    "tests/",
    "artifacts/",
    "logs/"
]

lista_arquivos = [
    "src/main.py",
    "src/config.py",
    ".env",
    "requirements.txt",    
]

for caminho in lista_caminhos:
    try:
        # os.makedirs cria todos os diretórios intermediários necessários
        os.makedirs(caminho, exist_ok=True)
        print(f"Estrutura de diretórios '{caminho}' criada com sucesso.")
    except OSError as e:
        print(f"Erro ao criar a estrutura '{caminho}': {e}")

for arquivo in lista_arquivos:
    try:
        # Cria um arquivo vazio   
        open(arquivo, "w").close()
        print(f"Arquivo '{arquivo}' criado com sucesso.")
    except OSError as e:
        print(f"Erro ao criar o arquivo '{arquivo}': {e}")