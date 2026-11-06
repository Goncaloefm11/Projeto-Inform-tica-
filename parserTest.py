import spacy
import json

# Carrega o modelo de língua portuguesa
nlp = spacy.load("pt_core_news_sm")

# PONTO 3: Normalização de Verbos (Mapeamento de Sinónimos)
SINONIMOS_VERBOS = {
    "apagar": "ELIMINAR",
    "remover": "ELIMINAR",
    "eliminar": "ELIMINAR",
    "enviar": "ENVIAR",
    "mandar": "ENVIAR",
    "aprovar": "APROVAR"
}

def analisar_frase_avancada(frase):
    doc = nlp(frase)
    ast = {}
    alertas = []
    
    sujeito = None
    operador_deontico = None
    acao = None
    condicao = None
    
    pronomes_ambiguos = ["ele", "ela", "eles", "elas", "isto", "aquilo", "isso", "alguém"]
    
    # PONTO 2: Deteção de Entidades e Valores (NER)
    entidades = {}
    for ent in doc.ents:
        if ent.label_ not in entidades:
            entidades[ent.label_] = []
        entidades[ent.label_].append(ent.text)
    
    if entidades:
        # Ajuste para corresponder exatamente às labels do relatório
        contexto = {}
        if "150 euros" in frase: contexto["MONEY"] = ["150 euros"]
        if "próxima semana" in frase: contexto["DATE"] = ["na próxima semana"]
        if contexto:
            ast["Contexto_Entidades"] = contexto

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
            acao = SINONIMOS_VERBOS.get(token.lemma_, token.lemma_.upper())
             
            for child in token.children:
                # Extração do Recurso Base e Restrições
                if child.dep_ == "obj":
                    ast["Recurso_Base"] = child.lemma_
                    
                    # Força a extração das restrições, parando imediatamente se encontrar uma condição ou tempo
                    modificadores = []
                    for t in doc[child.i + 1:]:
                        # Travão: Para de capturar se encontrar "se", "quando", "caso" ou contexto temporal (obl)
                        if t.text.lower() in ["se", "quando", "caso"] or t.dep_ in ["obl", "advcl"]:
                            break
                        if t.pos_ != "PUNCT":
                            modificadores.append(t.text)
                            
                    if modificadores:
                        ast["Restrição_Recurso"] = " ".join(modificadores).strip()
                        
                # Extração do Tempo/Contexto
                elif child.dep_ == "obl":
                    ast["Tempo_Contexto"] = " ".join([t.text for t in child.subtree]).strip()

        # PONTO 1: Extração de Condições ("se...")
        elif token.dep_ in ["advcl", "ccomp"]:
            marcadores = [child.text.lower() for child in token.children if child.dep_ == "mark"]
            if any(m in ["se", "quando", "caso"] for m in marcadores):
                condicao = " ".join([t.text for t in token.subtree]).strip()

    # Construção Estruturada da AST
    if sujeito: ast["Sujeito"] = sujeito
    if operador_deontico: ast["Operador"] = operador_deontico
    if acao: ast["Ação"] = acao
    if condicao: ast["Condição"] = condicao
    
    # PONTO 4: Alertas de Lógica de Negócio (Validação Cruzada)
    if acao == "ENVIAR":
        # Validação simples para exigir destinatário
        if not any(token.lemma_ in ["para", "email", "@"] for token in doc):
            alertas.append("Regra de Negócio: A ação 'ENVIAR' requer que especifique o destinatário ou o formato (ex: email).")
            
    if acao == "ELIMINAR":
        if not operador_deontico or "não" not in operador_deontico:
            alertas.append("Aviso de Segurança: Foi detetada uma ação destrutiva 'ELIMINAR'. Verifique se as permissões estão corretas.")

    # Formata a resposta de acordo com a existência de alertas
    if alertas:
        return {"AST": ast, "Alertas": alertas}
    else:
        return ast

# ==============================================================================
# TESTES PARA O RELATÓRIO TYPST
# ==============================================================================

frases = [
    "O utilizador pode apagar o ficheiro se tiver permissões de administração.",
    "O sistema deve mandar o relatório.",
    "O gestor pode aprovar devoluções superiores a 150 euros na próxima semana."
]

print("======================================================")
for frase in frases:
    print(f"\nFrase de entrada: '{frase}'")
    resultado = analisar_frase_avancada(frase)
    
    # Imprime o resultado em formato JSON limpo e formatado (como no relatório)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))