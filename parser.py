import re

# 1. Analisador Léxico Unificado (Vocabulário de Domínio I)
sujeitos = r"O administrador|O utilizador|O sistema"
operadores = r"pode|não pode|tem de"
acoes_deonticas = r"eliminar|alterar|se autenticar|editar"
verbos_analiticos = r"mostra|lista|identifica|faz|cria"
recursos = r"utilizadores|um pedido|um utilizador|a quantidade de anulações por operador|um histograma do número de transações rejeitadas por POS"
condicoes = r"sem permissão de edição|antes de aceder aos dados|se possuir permissão de gestão"

# 2. Analisador Sintático (Regras Gramaticais Gerais baseadas na EBNF)
padrao= re.compile(rf"^({sujeitos})\s+({operadores})\s+({acoes_deonticas})(?:\s+({recursos}))?(?:\s+({condicoes}))?\.$", re.IGNORECASE)

def analisar_frase(frase):
    # A função testa a gramática geral (tenta as várias ramificações possíveis)
    frase_limpa = frase.strip()
    
    match = padrao.match(frase_limpa)
    if match:
        return {
            "Sujeito": match.group(1),
            "Operador": match.group(2),
            "Acao": match.group(3),
            "Recurso": match.group(4),   
            "Condicao": match.group(5)
        }
        
    raise ValueError(f"Erro Sintático: Frase inválida ou fora da gramática geral -> '{frase}'")

# Teste com frases de ambos os domínios
frases = [
    "O administrador pode eliminar utilizadores.",
    "O utilizador não pode alterar um pedido sem permissão de edição.",
    "O utilizador tem de se autenticar antes de aceder aos dados.",
    "O administrador pode eliminar um utilizador se possuir permissão de gestão.",
    "O sistema mostra a quantidade de anulações por operador no último mês.",
    "O sistema cria um histograma do número de transações rejeitadas por POS."
]

for frase in frases:
    print(f"Frase: {frase}")
    try:
        arvore_ast = analisar_frase(frase)
        for chave, valor in arvore_ast.items():
            if valor is not None:
                print(f"  {chave}: {valor}")
    except ValueError as e:
        print(f"  {e}")
    print("-" * 50)