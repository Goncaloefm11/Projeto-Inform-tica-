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

# ----------------------------------------------------------------------
# 3. Analisador Léxico (Vocabulário do Domínio II)
# ----------------------------------------------------------------------
verbos_reativos = r"envia|gera|emite|sinaliza|bloqueia"
recursos_alerta = r"um email de alerta|um email|um aviso por email"
destinatarios = r"o supervisor de loja|o supervisor|a equipa de auditoria|a equipa de segurança|a equipa de seguranca|[\w.-]+@[\w.-]+\.\w+"
anexos = r"o relatório|o relatorio|os detalhes da transação|os detalhes da transacao"

verbos_analiticos = r"mostra|lista|identifica"
verbos_visualizacao = r"faz|cria|mostra"
graficos = (
    r"um gráfico de (?:barras|linhas|dispersão|dispersao|circular|temporal)|"
    r"um grafico de (?:barras|linhas|dispersão|dispersao|circular|temporal)|"
    r"um gráfico temporal|um grafico temporal|um mapa de calor|um histograma"
)
dimensoes = r"operador|loja|terminal|POS|cliente|método de reembolso|metodo de reembolso"
janelas_temporais = (
    r"no último mês|no ultimo mes|nos últimos \d+ dias|nos ultimos \d+ dias|"
    r"nos últimos \d+ meses|nos ultimos \d+ meses|na última semana|na ultima semana|"
    r"no mesmo mês|no mesmo mes|na mesma semana|no mesmo turno|na mesma hora"
)

padrao_reativa = re.compile(
    rf"^Se\s+(?P<CondicaoEvento>.*?)(?:,|\s+então|\s+entao)?\s+o sistema\s+"
    rf"(?P<AcaoReativa>{verbos_reativos})\s+"
    rf"(?P<RecursoAlerta>{recursos_alerta})"
    rf"(?:\s+com\s+(?P<Anexo_1>{anexos}))?"
    rf"(?:\s+para\s+(?P<Destinatario>{destinatarios}))?"
    rf"(?:\s+com\s+(?P<Anexo_2>{anexos}))?\.$",
    re.IGNORECASE
)

padrao_analitica = re.compile(
    rf"^O sistema\s+(?P<Verbo>{verbos_analiticos})\s+"
    rf"(?P<Metrica>.*?)"
    rf"(?:\s+por\s+(?P<Agrupamento>{dimensoes}))?"
    rf"(?:\s+(?P<JanelaTemporal>{janelas_temporais}))?\.$",
    re.IGNORECASE
)

# 2.3 Diretiva de Visualização (Text-to-Dashboard)
padrao_visualizacao = re.compile(
    rf"^O sistema\s+(?P<Verbo>{verbos_visualizacao})\s+"
    rf"(?P<Grafico>{graficos})"
    rf"(?:\s+(?:com|da|de|das|dos|do)\s+(?P<Metrica>.*?))?"
    rf"(?:\s+por\s+(?P<Agrupamento>{dimensoes}))?"
    rf"(?:\s+(?P<Contexto>durante .*?))?\.$",
    re.IGNORECASE
)

# ----------------------------------------------------------------------
# 4. Analisador Sintático 
# ----------------------------------------------------------------------
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
    m_reativa = padrao_reativa.match(frase_limpa)
    if m_reativa:
        ast = {"Regra_EBNF": "RegraReativa"}
        raw_dict = m_reativa.groupdict()
        anexo = raw_dict.get("Anexo_1") or raw_dict.get("Anexo_2")
        
        ast["CondicaoEvento"] = raw_dict["CondicaoEvento"].strip()
        ast["AcaoReativa"] = raw_dict["AcaoReativa"].strip()
        ast["RecursoAlerta"] = raw_dict["RecursoAlerta"].strip()
        if raw_dict.get("Destinatario"):
            ast["Destinatario"] = raw_dict["Destinatario"].strip()
        if anexo:
            ast["Anexo"] = anexo.strip()
        return ast

    # 3. Domínio II — Consulta Analítica (Text-to-SQL)
    m_analitica = padrao_analitica.match(frase_limpa)
    if m_analitica:
        ast = {"Regra_EBNF": "ConsultaAnalitica"}
        ast.update({k: v.strip() for k, v in m_analitica.groupdict().items() if v is not None})
        return ast

    # 4. Domínio II — Diretiva de Visualização (Text-to-Dashboard)
    m_visualizacao = padrao_visualizacao.match(frase_limpa)
    if m_visualizacao:
        ast = {"Regra_EBNF": "DiretivaVisualizacao"}
        ast.update({k: v.strip() for k, v in m_visualizacao.groupdict().items() if v is not None})
        return ast

    raise ValueError(f"Erro Sintático: Frase inválida ou fora da gramática geral -> '{frase}'")

# Teste com frases de ambos os domínios
frases = [
    # Domínio I
    "O administrador pode eliminar utilizadores.",
    "O utilizador não pode alterar um pedido sem permissão de edição.",
    "O utilizador tem de se autenticar antes de aceder aos dados.",
    "O administrador pode eliminar um utilizador se possuir permissão de gestão.",

    #Domínio II 
    "O sistema mostra a quantidade de anulações por operador no último mês.",
    "O sistema cria um histograma do número de transações rejeitadas por POS.",
    "O sistema mostra a quantidade de anulações por operador no último mês.",
    "O sistema lista as transações onde o valor acumulado de anulações foi superior a 150 euros.",
    "O sistema faz um gráfico de barras com o top 10 de operadores com maior taxa de anulação, de linhas.",
    "O sistema cria um gráfico temporal com a evolução diária de talões anulados por loja.",
    "Se um operador anular mais de 5 talões no mesmo turno, o sistema envia um email de alerta com o relatório para o supervisor.",
    "O sistema mostra o total de reembolsos em numerário sem talão de compra nos últimos 30 dias.",
    "O sistema lista os clientes com mais de 3 devoluções no mesmo mês.",
    "O sistema cria um gráfico circular com a distribuição de devoluções por método de reembolso.",
    "O sistema faz um gráfico de dispersão correlacionando o valor das devoluções com a hora do dia.",
    "Se um cliente solicitar mais de 3 devoluções na mesma semana então o sistema envia um email para a equipa de auditoria.",
    "O sistema mostra todos os artigos com alteração manual de PVP superior a 20 por cento na última semana.",
    "O sistema lista os operadores que executaram reduções de PVP sem registo de motivo.",
    "O sistema faz um gráfico de linhas comparando a margem esperada versus a margem real após alterações de PVP.",
    "O sistema mostra um mapa de calor das lojas com maior volume de descontos manuais no preço.",
    "Se o valor do desconto manual exceder 15 euros então o sistema envia um aviso por email para o supervisor de loja com os detalhes da transação.",
    "O sistema mostra a quantidade de clientes com mais de 5 transações completadas por mês nos últimos 5 meses.",
    "O sistema identifica os cartões de fidelização associados a compras em mais de 2 terminais na mesma hora",
    "O sistema cria um histograma do número de transações rejeitadas por POS.",
    "O sistema faz um gráfico de barras com a velocidade média de vendas por operador durante os períodos de pico.",
    "Se um terminal registar mais de 3 transações rejeitadas consecutivas então o sistema envia um email para eu@eu.eu."
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