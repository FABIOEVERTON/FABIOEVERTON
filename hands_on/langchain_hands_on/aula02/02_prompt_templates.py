"""
Aula 02: Prompt Templates e Output Parsing
Prompt Template = um "molde" para perguntas, onde voce preenche variaveis
Output Parser = transforma a resposta textual do modelo em algo estruturado (dicionario, lista, etc.)

Analogia:
- Prompt Template = formulario com campos em branco
- Output Parser = extrator que pega a resposta e organiza em caixinhas
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

modelo = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# =============================================
# 1. PROMPT TEMPLATE BASICO
# =============================================
# O template tem {variaveis} que sao preenchidas depois
template = ChatPromptTemplate.from_messages([
    ("system", "Voce e um especialista em {area}."),
    ("human", "Explique o conceito de {conceito} para um iniciante.")
])

# Preenchendo as variaveis
mensagem = template.invoke({
    "area": "Inteligencia Artificial",
    "conceito": "LangChain"
})

print("=== PROMPT MONTADO ===")
print(mensagem)
print()

resposta = modelo.invoke(mensagem)
print("=== RESPOSTA ===")
print(resposta.content)
print()

# =============================================
# 2. STR OUTPUT PARSER
# =============================================
# O StrOutputParser simplesmente extrai o texto da resposta
parser = StrOutputParser()

# Chain = Template -> Modelo -> Parser
# O operador | (pipe) conecta as etapas
chain = template | modelo | parser

resultado = chain.invoke({
    "area": "Programacao",
    "conceito": "Orientacao a Objetos"
})

print("=== CHAIN COMPLETA (Template | Modelo | Parser) ===")
print(resultado)
print()

# =============================================
# 3. MULTIPLOS PROMPTS EM SEQUENCIA
# =============================================
tradutor = ChatPromptTemplate.from_messages([
    ("system", "Traduza o texto a seguir para {idioma}.")
])

revisor = ChatPromptTemplate.from_messages([
    ("system", "Voce e um revisor. Corrija erros e melhore o texto a seguir.")
])

chain_traducao = tradutor | modelo | parser
chain_revisao = revisor | modelo | parser

texto_original = "LangChain is a framework for developing applications powered by language models."

traduzido = chain_traducao.invoke({"idioma": "portugues brasileiro", "texto": texto_original})
print("=== TRADUZIDO ===")
print(traduzido)

revisado = chain_revisao.invoke({"texto": traduzido, "idioma": "portugues brasileiro"})
print()
print("=== REVISADO ===")
print(revisado)
