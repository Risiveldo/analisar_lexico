import re

# Definição de padrões (regex) para os tokens
token_patterns = [
    (r'program|var|integer|real|boolean|procedure|begin|end|if|then|else|while|do|not', 'PalavraChave'),
    (r'[a-zA-Z][a-zA-Z0-9_]*', 'Identificador'),
    (r'\d+\.\d*', 'NumeroReal'),
    (r'\d+', 'NumeroInteiro'),
    (r';|\.|:|\(|\)|,', 'Delimitador'),
    (r':=', 'ComandoAtribuicao'),
    (r'=|<=|>=|<>|<|>', 'OperadorRelacional'),
    (r'\+|-|or', 'OperadorAditivo'),
    (r'\*|/|and', 'OperadorMultiplicativo'),
]

# Expressões regulares para ignorar espaços e comentários
ignorar_espacos = r'\s+'
comentario_simples = r'{[^}]*}'  # Comentários simples entre chaves
comentario_nao_fechado = r'{[^}]*$'  # Comentário não fechado

# Função para verificar se um token corresponde a um símbolo inválido
def simbolo_invalido(token):
    return re.match(r'[^a-zA-Z0-9_;\.\:=\(\),\*/+-]', token)

# Função para o analisador léxico
def analisador_lexico(codigo):
    linhas = codigo.splitlines()
    tabela_simbolos = []
    erros = []

    for num_linha, linha in enumerate(linhas, start=1):
        # Ignorar espaços em branco e comentários
        linha = re.sub(comentario_simples, '', linha)
        
        if re.search(comentario_nao_fechado, linha):
            erros.append(f"Erro na linha {num_linha}: Comentário não fechado.")
            continue

        # Remover espaços em branco
        linha = re.sub(ignorar_espacos, '', linha)
        
        pos = 0
        while pos < len(linha):
            token = None
            tipo = None
            
            # Tentar encontrar cada padrão de token
            for pattern, token_type in token_patterns:
                match = re.match(pattern, linha[pos:])
                if match:
                    token = match.group(0)
                    tipo = token_type
                    break

            if token:
                tabela_simbolos.append((token, tipo, num_linha))
                pos += len(token)
            else:
                # Verificar se o símbolo é inválido
                if simbolo_invalido(linha[pos]):
                    erros.append(f"Erro na linha {num_linha}: Símbolo inválido '{linha[pos]}'.")
                    pos += 1
                else:
                    pos += 1

    return tabela_simbolos, erros

# Função para ler o arquivo e passar para o analisador léxico
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file:
            codigo = file.read()
        return codigo
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None

# Testando o analisador léxico com um arquivo
def analisar_arquivo(nome_arquivo):
    codigo = ler_arquivo(nome_arquivo)
    if codigo is not None:
        tabela_simbolos, erros = analisador_lexico(codigo)

        # Mostrando a tabela de símbolos e erros
        if tabela_simbolos:
            print("Tabela de Símbolos:")
            for token, tipo, linha in tabela_simbolos:
                print(f"Token: {token}, Tipo: {tipo}, Linha: {linha}")

        if erros:
            print("\nErros:")
            for erro in erros:
                print(erro)

# Exemplo de como rodar o código para analisar um arquivo
if __name__ == "__main__":
    # Solicita o nome do arquivo ao usuário
    nome_arquivo = input("Digite o nome do arquivo para analisar: ")
    analisar_arquivo(nome_arquivo)
