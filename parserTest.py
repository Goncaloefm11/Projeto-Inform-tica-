import re

# ==============================================================================
# 1. GRAMÁTICA EBNF (Tradução para Expressões Regulares)
# ==============================================================================

# Regra EBNF 1: SentencaDeontica (Domínio I)
regex_deontica = re.compile(
    r"^(?P<Sujeito>(?:O|A|Os|As|Um|Uma)?\s*(?:administrador|utilizador|operador|supervisor|cliente|gestor)(?:\s+(?:com perfil de leitura|de loja))?)\s+"
    r"(?P<Operador>pode|não pode|tem de)\s+"
    r"(?P<Acao>eliminar|alterar|se autenticar|editar|criar|consultar|aceder|aprovar|descarregar)\b"
    r"(?:\s+(?P<Recurso>(?:O|A|Os|As|Um|Uma)?\s*(?:utilizadores|dados|pedido|permissao de edicao|talao|PVP|um pedido|um utilizador|permissões|ao sistema|o documento|o recurso)))?"
    r"(?:\s+(?P<Condicao>(?:se|antes de|sem)\s+.*))?\.$", 
    re.IGNORECASE
)

# Regra EBNF 2: RegraReativa (Domínio II - Event-Condition-Action)
regex_reativa = re.compile(
    r"^Se\s+(?P<CondicaoEvento>.*?)\s+"
    r"então o sistema\s+"
    r"(?P<AcaoReativa>envia|gera|emite|sinaliza|bloqueia)\s+"
    r"(?P<RecursoAlerta>um email de alerta|um email|um aviso por email)"
    r"(?:\s+com\s+(?P<Anexo>o relatorio|os detalhes da transacao))?"
    r"(?:\s+para\s+(?P<Destinatario>o supervisor de loja|o supervisor|a equipa de auditoria|a equipa de seguranca|eu@eu\.eu))?\.$",
    re.IGNORECASE
)

# Regra EBNF 3: ConsultaAnalitica (Domínio II - Text-to-SQL)
regex_analitica = re.compile(
    r"^O sistema\s+"
    r"(?P<VerboConsulta>mostra|lista|identifica)\s+"
    r"(?P<RecursoAnalitico>.*?)"
    r"(?:\s+por\s+(?P<Agrupamento>operador|loja|terminal|POS|cliente|metodo de reembolso))?"
    r"(?:\s+(?P<Tempo>no ultimo mes|nos ultimos \d+ dias|nos ultimos \d+ meses|na ultima semana|na mesma semana|no mesmo turno|na mesma hora))?\.$",
    re.IGNORECASE
)

# Regra EBNF 4: DiretivaVisualizacao (Domínio II - Text-to-Dashboard)
regex_visualizacao = re.compile(    
    r"^O sistema\s+"
    r"(?P<VerboVisualizacao>faz|cria|mostra)\s+"
    r"(?P<Grafico>um grafico de (?:barras|linhas|dispersao|circular|temporal)|um mapa de calor|um histograma)\s+"
    r"(?:com|do)\s+"
    r"(?P<Recurso>.*?)"
    r"(?:\s+por\s+(?P<Agrupamento>operador|loja|terminal|POS|cliente|metodo de reembolso))?\.$",
    re.IGNORECASE
)

# ==============================================================================
# 2. ANALISADOR SINTÁTICO (Parser)
# ==============================================================================

def analisar_frase(frase):
    frase_limpa = frase.strip()
    
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
# 3. CAMADA DE SUPORTE SUPLEMENTAR 
# ==============================================================================

regex_reativa_ext = re.compile(
    r"^Se\s+(?P<CondicaoEvento>.*?)(?:,|\s+então|\s+entao)?\s+o sistema\s+"
    r"(?P<AcaoReativa>envia|gera|emite|sinaliza|bloqueia)\s+"
    r"(?P<RecursoAlerta>um email de alerta|um email|um aviso por email)"
    r"(?:\s+com\s+(?P<Anexo_1>o relatório|o relatorio|os detalhes da transação|os detalhes da transacao))?"
    r"(?:\s+para\s+(?P<Destinatario>o supervisor de loja|o supervisor|a equipa de auditoria|a equipa de segurança|a equipa de seguranca|[\w.-]+@[\w.-]+\.\w+))?"
    r"(?:\s+com\s+(?P<Anexo_2>o relatório|o relatorio|os detalhes da transação|os detalhes da transacao))?\.$",
    re.IGNORECASE
)

regex_analitica_ext = re.compile(
    r"^O sistema\s+(?P<VerboConsulta>mostra|lista|identifica)\s+(?P<RecursoAnalitico>.*?)"
    r"(?:\s+por\s+(?P<Agrupamento>operador|loja|terminal|POS|cliente|método de reembolso|metodo de reembolso))?"
    r"(?:\s+(?P<Tempo>no último mês|no ultimo mes|nos últimos \d+ dias|nos ultimos \d+ dias|nos últimos \d+ meses|nos ultimos \d+ meses|na última semana|na ultima semana|no mesmo mês|no mesmo mes|na mesma semana|no mesmo turno|na mesma hora))?\.$",
    re.IGNORECASE
)

regex_visualizacao_ext = re.compile(
    r"^O sistema\s+(?P<VerboVisualizacao>faz|cria|mostra)\s+"
    r"(?P<Grafico>um gráfico (?:de\s+)?(?:barras|linhas|dispersão|dispersao|circular|temporal)|"
    r"um grafico (?:de\s+)?(?:barras|linhas|dispersao|circular|temporal)|"
    r"um gráfico temporal|um grafico temporal|um mapa de calor|um histograma)"
    r"(?:\s+(?:com|do|da|dos|das|de|comparando|correlacionando)\s+(?P<Recurso>.*?))?"
    r"(?:\s+por\s+(?P<Agrupamento>operador|loja|terminal|POS|cliente|método de reembolso|metodo de reembolso))?"
    r"(?:\s+(?P<Contexto>durante .*?))?\.$",
    re.IGNORECASE
)

def analisar_frase_completa(frase):
    frase_formatada = frase.strip()
    if not frase_formatada.endswith("."):
        frase_formatada += "."

    # 1. Tenta a função inicial
    try:
        return analisar_frase(frase_formatada)
    except ValueError:
        pass

    # 2. Se falhar por acentuação ou conectores adicionais, usa a extensão
    m_reativa = regex_reativa_ext.match(frase_formatada)
    if m_reativa:
        ast = m_reativa.groupdict()
        ast["Regra_EBNF"] = "RegraReativa"
        anexo = ast.pop("Anexo_1", None) or ast.pop("Anexo_2", None)
        if anexo:
            ast["Anexo"] = anexo
        return {k: v for k, v in ast.items() if v is not None}

    m_analitica = regex_analitica_ext.match(frase_formatada)
    if m_analitica:
        ast = m_analitica.groupdict()
        ast["Regra_EBNF"] = "ConsultaAnalitica"
        return {k: v for k, v in ast.items() if v is not None}

    m_visualizacao = regex_visualizacao_ext.match(frase_formatada)
    if m_visualizacao:
        ast = m_visualizacao.groupdict()
        ast["Regra_EBNF"] = "DiretivaVisualizacao"
        return {k: v for k, v in ast.items() if v is not None}

    raise ValueError(f"Erro Sintático: A frase não corresponde a nenhuma regra da EBNF -> '{frase_formatada}'")


# ==============================================================================
# 4. TESTES UNIFICADA (DOMÍNIO I & DOMÍNIO II)
# ==============================================================================

frases_teste_unificadas = [
    # --- DOMÍNIO I: Políticas Deônticas de Controlo de Acesso ---
    "O administrador pode eliminar utilizadores.",
    "O utilizador não pode alterar um pedido sem permissão de edição.",
    "O utilizador tem de se autenticar antes de aceder aos dados.",
    "O administrador pode eliminar um utilizador se possuir permissão de gestão.",

    # --- DOMÍNIO II: Auditoria Operacional e Deteção de Risco ---
    "O sistema mostra a quantidade de anulações por operador no último mês.",
    "O sistema lista as transações onde o valor acumulado de anulações foi superior a 150 euros.",
    "O sistema faz um gráfico de barras com o top 10 de operadores com maior taxa de anulação de linhas.",
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
    "O sistema identifica os cartões de fidelização associados a compras em mais de 2 terminais na mesma hora.",
    "O sistema cria um histograma do número de transações rejeitadas por POS.",
    "O sistema faz um gráfico de barras com a velocidade média de vendas por operador durante os períodos de pico.",
    "Se um terminal registar mais de 3 transações rejeitadas consecutivas então o sistema envia um email para eu@eu.eu."
]

if __name__ == "__main__":
    print("=== Testes de Análise Sintática (DOMÍNIO I & II) ===")
    print("=" * 70)
    
    sucesso = 0
    falhas = 0

    for i, frase in enumerate(frases_teste_unificadas, 1):
        print(f"[{i:02d}] Frase: {frase}")
        try:
            ast = analisar_frase_completa(frase)
            sucesso += 1
            for chave, valor in ast.items():
                print(f"  * {chave}: {valor}")
        except ValueError as e:
            falhas += 1
            print(f"  [ERRO] {e}")
        print("-" * 70)

    print(f"\nResumo da Execução:")
    print(f"  * Frases analisadas com sucesso: {sucesso}/{len(frases_teste_unificadas)}")
    print(f"  * Erros sintáticos: {falhas}")