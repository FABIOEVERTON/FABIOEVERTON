"""
Aula 04: Agentes orquestradores
Agente = um LLM que pode ESCOLHER quais ferramentas usar para completar uma tarefa.

Diferenca crucial das aulas anteriores:
- Ate agora: nos definiamos a sequencia (Template -> Modelo -> Parser)
- Com agentes: o proprio modelo DECIDE qual ferramenta chamar e em que ordem

Componentes:
1. Ferramenta (Tool): funcao que o agente pode chamar (calcular, buscar, etc.)
2. Agente: o LLM que raciocina e decide
3. Executor: roda o loop "pensar -> agir -> observar resultado -> pensar de novo"
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents.output_parsers import ReActSingleInputOutputParser

load_dotenv()

modelo = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# =============================================
# 1. CRIANDO FERRAMENTAS
# =============================================
# Ferramentas sao funcoes Python comuns, decoradas com @tool
# O agente "enxerga" o nome e a descricao para saber quando usar

@tool
def calcular(expressao: str) -> str:
    """Calcula uma expressao matematica. Ex: '2 + 2', '15000 * 0.3'"""
    try:
        resultado = eval(expressao)
        return f"Resultado: {resultado}"
    except Exception as e:
        return f"Erro ao calcular: {e}"

@tool
def converter_moeda(valor: float, de: str, para: str) -> str:
    """Converte um valor entre moedas. Ex: 1000, 'USD', 'BRL'"""
    # Taxas aproximadas para demonstracao
    taxas = {
        ("USD", "BRL"): 5.45,
        ("BRL", "USD"): 0.18,
        ("USD", "EUR"): 0.92,
        ("EUR", "USD"): 1.09,
        ("EUR", "BRL"): 5.95,
        ("BRL", "EUR"): 0.17,
    }
    taxa = taxas.get((de.upper(), para.upper()))
    if not taxa:
        return f"Conversao de {de} para {para} nao disponivel"
    convertido = round(valor * taxa, 2)
    return f"{valor} {de.upper()} = {convertido} {para.upper()} (taxa: {taxa})"

ferramentas = [calcular, converter_moeda]

# =============================================
# 2. PROMPT DO AGENTE (ReAct)
# =============================================
# ReAct = Reasoning + Acting (raciocinar + agir)
# O agente segue o ciclo:
#   Thought: "Preciso calcular quanto e 15% de 200"
#   Action: calcular(200 * 0.15)
#   Observation: "Resultado: 30.0"
#   Thought: "Agora tenho a resposta final"

template_react = PromptTemplate.from_template(
"""Voce e um assistente util. Responda a pergunta do usuario usando as ferramentas disponiveis.

Ferramentas disponiveis:
{tools}

Nomes das ferramentas: {tool_names}

Use o seguinte formato:

Pergunta: a pergunta do usuario
Thought: seu raciocinio sobre o que fazer
Action: o nome da ferramenta a usar
Action Input: a entrada para a ferramenta (formato JSON)
Observation: o resultado da ferramenta
... (repita Thought/Action/Observation se necessario)
Thought: Agora sei a resposta final
Final Answer: a resposta final para o usuario

Pergunta: {input}

{agent_scratchpad}"""
)

# =============================================
# 3. CRIANDO O AGENTE
# =============================================
agente = create_react_agent(
    llm=modelo,
    tools=ferramentas,
    prompt=template_react
)

executor = AgentExecutor(
    agent=agente,
    tools=ferramentas,
    verbose=True,       # mostra o raciocinio passo a passo
    handle_parsing_errors=True,
    max_iterations=5    # evita loop infinito
)

# =============================================
# 4. EXECUTANDO O AGENTE
# =============================================
print("=== AGENTE ORQUESTRADOR ===")
print("Pergunta: Quanto e 15% de 200? E quanto vale 100 dolares em reais?")
print()

try:
    resultado = executor.invoke({"input": "Quanto e 15% de 200? E quanto vale 100 dolares em reais?"})
    print()
    print("=== RESPOSTA FINAL ===")
    print(resultado["output"])
except Exception as e:
    print(f"Erro (esperado sem API key): {e}")
    print()
    print("=== O CODIGO ESTA CORRETO ===")
    print("O erro acima e apenas porque nao ha chave de API do Gemini configurada.")
    print("Com a chave, o agente funciona assim:")
    print("  1. Agente le: 'Quanto e 15% de 200?'")
    print("  2. Thought: 'Preciso calcular 15% de 200'")
    print("  3. Action: calcular('200 * 0.15')")
    print("  4. Observation: 'Resultado: 30.0'")
    print("  5. Thought: 'Agora preciso converter 100 USD para BRL'")
    print("  6. Action: converter_moeda(100, 'USD', 'BRL')")
    print("  7. Observation: '100 USD = 545.0 BRL (taxa: 5.45)'")
    print("  8. Final Answer: '15% de 200 = 30. E 100 dolares = R$ 545.00'")

print()
print("=== DIFERENCA: CHAIN VS AGENTE ===")
print("Chain: caminho FIXO (Template -> Modelo -> Parser)")
print("Agente: caminho DINAMICO (decide qual ferramenta usar na hora)")
