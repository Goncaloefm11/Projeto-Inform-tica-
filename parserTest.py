import re

# ==============================================================================
# 1. GRAMÁTICA EBNF (Tradução para Expressões Regulares)
# ==============================================================================

# Regra EBNF 1: SentencaDeontica (Domínio I)
# SujeitoAgente OperadorDeontico AcaoOperacional RecursoSistema [ ClausulaCondicional ]
regex_deontica = re.compile(
    r"^(?P<Sujeito>O (?:administrador|utilizador|gestor|operador|cliente)(?:\s+(?:autenticado|não autenticado|com permissão de leitura|com perfil de leitura))?)\s+"
    r"(?P<Operador>não pode|pode|tem de)\s+"
    r"(?P<Acao>eliminar|alterar|se autenticar|editar|criar|consultar|aceder|aprovar|descarregar)\b"
    r"(?:\s+(?P<Recurso>utilizadores|um pedido|um utilizador|permissões|os dados|ao sistema|o documento|o recurso))?"
    r"(?:\s+(?P<Condicao>(?:se|antes de|sem)\s+.*))?\.$", 
    re.IGNORECASE
)

# Regra EBNF 2: RegraReativa (Domínio II - Event-Condition-Action)
# "Se" CondicaoEvento "entao" "o" "sistema" AcaoReativa [ "para" DestinatarioAlerta ]
regex_reativa = re.compile(
    r"^Se\s+(?P<CondicaoEvento>.*?)\s+"
    r"então o sistema\s+"
    r"(?P<AcaoReativa>envia|gera|emite|sinaliza|bloqueia)\s+"
    r"(?P<RecursoAlerta>.*?)"
    r"(?:\s+para\s+(?P<Destinatario>o supervisor.*|a equipa.*|eu@eu\.eu))?\.$",
    re.IGNORECASE
)

# Regra EBNF 3: ConsultaAnalitica (Domínio II - Text-to-SQL)
# "o" "sistema" VerboConsulta RecursoAnalitico [ AgrupamentoDimensao ] [ JanelaTemporal ]
regex_analitica = re.compile(
    r"^O sistema\s+"
    r"(?P<VerboConsulta>mostra|lista|identifica)\s+"
    r"(?P<RecursoAnalitico>.*?)"
    r"(?:\s+por\s+(?P<Agrupamento>operador|loja|terminal|POS|cliente|método de reembolso))?"
    r"(?:\s+(?P<Tempo>no último mês|nos últimos \d+ dias|na última semana|nos últimos \d+ meses))?\.$",
    re.IGNORECASE
)

# Regra EBNF 4: DiretivaVisualizacao (Domínio II - Text-to-Dashboard)
# "o" "sistema" VerboVisualizacao EspecificacaoGrafico "com" RecursoAnalitico [ AgrupamentoDimensao ]
regex_visualizacao = re.compile(
    r"^O sistema\s+"
    r"(?P<VerboVisualizacao>faz|cria|mostra)\s+"
    r"(?P<Grafico>um gráfico de .*?|um mapa de calor|um histograma)\s+"
    r"(?:com|do)\s+"
    r"(?P<Recurso>.*?)\.$",
    re.IGNORECASE
)

# ==============================================================================
# 2. ANALISADOR SINTÁTICO (Parser)
# ==============================================================================

def analisar_frase(frase):
    """
    Testa as várias ramificações da regra principal da EBNF:
    Regra ::= SentencaDeontica | RegraReativa | ConsultaAnalitica | DiretivaVisualizacao
    """
    frase_limpa = frase.strip()
    
    # 3. GERAÇÃO DA ÁRVORE DE SINTAXE ABSTRATA (AST) Tipada
    
    m_deontica = regex_deontica.match(frase_limpa)
    if m_deontica:
        ast = m_deontica.groupdict()
        ast["Regra_EBNF"] = "SentencaDeontica"
        return {k: v for k, v in ast.items() if v is not None}
        
    m_reativa = regex_reativa.match(frase_limpa)
    if m_reativa:
        ast = m_reativa.groupdict()
        ast["Regra_EBNF"] = "RegraReativa"
        return {k: v for k, v in ast.items() if v is not None}
        
    m_analitica = regex_analitica.match(frase_limpa)
    if m_analitica:
        ast = m_analitica.groupdict()
        ast["Regra_EBNF"] = "ConsultaAnalitica"
        return {k: v for k, v in ast.items() if v is not None}
        
    m_visualizacao = regex_visualizacao.match(frase_limpa)
    if m_visualizacao:
        ast = m_visualizacao.groupdict()
        ast["Regra_EBNF"] = "DiretivaVisualizacao"
        return {k: v for k, v in ast.items() if v is not None}
        
    raise ValueError(f"Erro Sintático: A frase não corresponde a nenhuma regra da EBNF -> '{frase}'")


# ==============================================================================
# TESTES
# ==============================================================================

frases_teste = [
    # Teste 1: SentencaDeontica
    "O administrador pode eliminar utilizadores.",
    "O utilizador não pode alterar um pedido sem permissão de edição.",
    
    # Teste 2: RegraReativa
    "Se um terminal registar mais de 3 transações rejeitadas consecutivas então o sistema envia um email para eu@eu.eu.",
    
    # Teste 3: ConsultaAnalitica
    "O sistema mostra a quantidade de anulações por operador no último mês.",
    
    # Teste 4: DiretivaVisualizacao
    "O sistema cria um histograma do número de transações rejeitadas por POS."
]

for frase in frases_teste:
    print(f"Frase Original: {frase}")
    try:
        arvore_ast = analisar_frase(frase)
        for chave, valor in arvore_ast.items():
            print(f"  {chave}: {valor}")
    except ValueError as e:
        print(f"  {e}")
    print("-" * 70)