import spacy

# Carrega o modelo de língua portuguesa
nlp = spacy.load("pt_core_news_sm")

# PONTO 3: Normalização de Verbos (Mapeamento de Sinónimos)
SINONIMOS_VERBOS = {
    "apagar": "ELIMINAR",
    "remover": "ELIMINAR",
    "eliminar": "ELIMINAR",
    "enviar": "ENVIAR",
    "mandar": "ENVIAR",
    "notificar": "ENVIAR",
    "ver": "CONSULTAR",
    "receber": "RECEBER",
    "consultar": "CONSULTAR"
}

def analisar_frase_avancada(frase):
    doc = nlp(frase)
    ast = {}
    alertas = []
    
    sujeito = None
    operador_deontico = None
    acao = None
    acao_original = None
    recurso = []
    condicao = None
    
    pronomes_ambiguos = ["ele", "ela", "eles", "elas", "isto", "aquilo", "isso", "alguém"]
    
    # PONTO 2: Deteção de Entidades e Valores (NER)
    entidades = {}
    for ent in doc.ents:
        if ent.label_ not in entidades:
            entidades[ent.label_] = []
        entidades[ent.label_].append(ent.text)
    
    if entidades:
        ast["Contexto_Entidades"] = entidades

    for token in doc:
        # Extração do Sujeito
        if "subj" in token.dep_:
            sujeito = " ".join([t.text for t in token.subtree]).strip()
            if token.pos_ == "PRON" and token.text.lower() in pronomes_ambiguos:
                 alertas.append(f"Alerta: O sujeito '{token.text}' é ambíguo. Quem é '{token.text}'?")
                 
        # Extração de Operadores Deônticos
        elif token.pos_ == "AUX" and token.lemma_ in ["poder", "dever", "ter"]:
            negacao = any(child.dep_ == "advmod" and child.text.lower() == "não" for child in token.head.children)
            prefixo = "não " if negacao else ""
            prep = next((child.text for child in token.children if child.dep_ == "mark" and child.text in ["de", "que"]), "")
            operador_deontico = f"{prefixo}{token.text} {prep}".strip()
                 
        # Extração da Ação (Verbo Principal)
        elif token.pos_ == "VERB" and (token.dep_ == "ROOT" or token.dep_ == "xcomp"):
            acao_original = token.lemma_
            # Aplica a Normalização (Ponto 3)
            acao = SINONIMOS_VERBOS.get(acao_original, acao_original.upper())
             
            # Extração de Recursos (Objetos) e Contexto (Tempo/Local)
            for child in token.children:
                # Se for o objeto direto (O Alvo da ação)
                if child.dep_ == "obj":
                    # Extrai apenas a palavra principal (ex: "devolução")
                    ast["Recurso_Base"] = child.lemma_
                        
                # Se for um modificador oblíquo (O Tempo ou Contexto)
                elif child.dep_ == "obl":
                    tempo_contexto = " ".join([t.text for t in child.subtree]).strip()
                    ast["Tempo_Contexto"] = tempo_contexto

        # PONTO 1: Extração de Condições ("se...")
        elif token.dep_ == "advcl" or token.dep_ == "ccomp":
            # Verifica se a cláusula começa com "se", "quando", "caso"
            marcadores = [child.text.lower() for child in token.children if child.dep_ == "mark"]
            if any(m in ["se", "quando", "caso"] for m in marcadores):
                condicao = " ".join([t.text for t in token.subtree]).strip()

    # Construção da Árvore
    if sujeito: ast["Sujeito"] = sujeito
    if operador_deontico: ast["Operador"] = operador_deontico
    if acao: ast["Ação"] = acao
    if recurso: ast["Recurso"] = " | ".join(recurso)
    if condicao: ast["Condição"] = condicao
    
    # PONTO 4: Alertas de Lógica de Negócio (Validação Cruzada)
    if acao == "ENVIAR":
        texto_recursos = str(recurso).lower()
        if "@" not in texto_recursos and "email" not in texto_recursos and "para" not in texto_recursos:
            alertas.append("Regra de Negócio: A ação 'ENVIAR' requer que especifique o destinatário ou o formato (ex: email).")
            
    if acao == "ELIMINAR":
        if not operador_deontico or "não" not in operador_deontico:
            alertas.append("Aviso de Segurança: Foi detetada uma ação destrutiva 'ELIMINAR'. Verifique se as permissões estão corretas.")

    return {"AST": ast, "Alertas": alertas}


# ==============================================================================
# TESTAR AS 4 NOVAS FUNCIONALIDADES
# ==============================================================================

frases = [
    # Testa Normalização ("apagar" -> ELIMINAR), Alerta de Segurança, e Condição ("se...")
    "O utilizador pode apagar o ficheiro se tiver permissões de administração.",
    
    # Testa Alerta de Lógica de Negócio (falta destinatário)
    "O sistema deve mandar o relatório.",
    
    # Testa Deteção de Entidades (Valores, Dinheiro, Datas)
    "O gestor pode aprovar devoluções superiores a 150 euros na próxima semana."
]

print("======================================================")
for frase in frases:
    print(f"\nFrase: '{frase}'")
    resultado = analisar_frase_avancada(frase)
    
    print("Árvore Extraída:")
    for chave, valor in resultado["AST"].items():
        print(f"  - {chave}: {valor}")
        
    if resultado["Alertas"]:
        print("Interação / Alertas:")
        for alerta in resultado["Alertas"]:
            print(f"  [!] {alerta}")
    else:
        print("  [OK] Frase válida")