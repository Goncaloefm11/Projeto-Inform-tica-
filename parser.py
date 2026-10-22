import re

# 1. Analisador Léxico
sujeitos = r"O administrador|O utilizador"
operadores = r"pode|não pode|tem de"
acoes = r"eliminar|alterar|se autenticar|editar"
recursos = r"utilizadores|um pedido|um utilizador"
condicoes = r"sem permissão de edição|antes de aceder aos dados|se possuir permissão de gestão"

# 2. Analisador Sintático (Regras Gramaticais)
# O (?: ...)? indica que o bloco inteiro (espaço + recurso/condição) é opcional, 
# mas o grupo de captura lá dentro regista a palavra se ela existir.
padrao_deontico = re.compile(rf"^({sujeitos})\s+({operadores})\s+({acoes})(?:\s+({recursos}))?(?:\s+({condicoes}))?\.$", re.IGNORECASE)

def analisar_frase(frase):
    match = padrao_deontico.match(frase.strip())
    
    if match:
        # 3. Geração da AST
        ast = {
            "Sujeito": match.group(1),
            "Operador": match.group(2),
            "Acao": match.group(3),
            "Recurso": match.group(4),   
            "Condicao": match.group(5)
        }
        return ast
    else:
        raise ValueError(f"Erro Sintático: Frase inválida ou fora do vocabulário -> '{frase}'")

# Teste com a lista de frases
frases = [
    "O administrador pode eliminar utilizadores.",
    "O utilizador não pode alterar um pedido sem permissão de edição.",
    "O utilizador tem de se autenticar antes de aceder aos dados.",
    "O administrador pode eliminar um utilizador se possuir permissão de gestão."
    #,"O sistema mostra a quantidade de anulações por operador no último mês.",
    #"O sistema cria um histograma do número de transações rejeitadas por POS."
]

for frase in frases:
    arvore_ast = analisar_frase(frase)
    print(f"Frase: {frase}")
    for chave, valor in arvore_ast.items():
        if valor is not None:
            print(f"  {chave}: {valor}")
    print("-" * 50) 