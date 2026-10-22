# Projeto-Inform-tica-
Implementação em Python de um fragmento de Português Controlado (MOCL) para converter regras corporativas (controlo de acessos e auditoria) numa AST determinística. A solução elimina ambiguidades e alucinações de LLMs, assegurando a verificação formal e segura de políticas de negócio.


# Linguagem Natural Controlada para Regras Corporativas

Implementação em Python de um fragmento de Português Controlado (MOCL) para converter regras corporativas (controlo de acessos e auditoria) numa Árvore de Sintaxe Abstrata (AST) determinística. A solução elimina ambiguidades e alucinações de LLMs, assegurando a verificação formal e segura de políticas de negócio.

## 📌 Sobre o Projeto

Este projeto está a ser desenvolvido no âmbito da Dissertação de Mestrado em Engenharia Informática na **Universidade do Minho**.

A formulação de regras organizacionais em linguagem natural livre encerra desafios críticos de ambiguidade semântica. Embora os Modelos de Linguagem de Grande Escala (LLMs) ofereçam traduções rápidas para código, a sua natureza probabilística introduz riscos inaceitáveis de alucinações e não-determinismo em sistemas críticos. 

Para resolver isto, o nosso sistema utiliza uma abordagem rigorosa e formal baseada numa gramática livre de contexto (EBNF), focando-se em dois domínios corporativos:
1. **Controlo de Acessos (Domínio I):** Políticas deônticas baseadas em permissões, proibições e obrigações.
2. **Auditoria Transacional (Domínio II):** Monitorização de risco, anulações atípicas e consultas analíticas no retalho.

## ⚙️ Arquitetura do Sistema

O pipeline de processamento em Python divide-se em três fases sequenciais:
1. **Analisador Léxico (Lexer):** Segmentação e classificação de *tokens* com base num dicionário controlado rigoroso.
2. **Analisador Sintático (Parser):** Validação sintática determinística através de expressões regulares adaptadas à gramática do projeto.
3. **Geração da AST:** Transformação da frase validada numa estrutura de dados tipada (Árvore de Sintaxe Abstrata), pronta a ser transposta para código executável.

## 🚀 Como Executar

**Pré-requisitos:**
* Python 3.x (Não requer bibliotecas externas além da standard library `re`).
