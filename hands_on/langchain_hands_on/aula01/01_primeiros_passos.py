"""
Aula 01: Primeiros passos com o LangChain
O que e LangChain? Um framework que conecta seu codigo a LLMs (como Gemini, GPT)
de forma estruturada, usando "cadeias" (chains) de passos.

Conceitos:
- LLM: modelo de linguagem (ex: Gemini)
- Prompt: instrucao que voce da para o modelo
- Chain: sequencia de passos que o codigo executa
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# 1. CONECTAR AO MODELO
# O LangChain cria uma interface unica para falar com qualquer LLM
# Aqui usamos Gemini do Google
modelo = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7  # 0 = deterministico, 1 = criativo
)

# 2. PRIMEIRA CHAMADA SIMPLES
# O metodo invoke() envia uma mensagem e recebe a resposta
resposta = modelo.invoke("Explique em uma frase o que e LangChain")
print("=== RESPOSTA 1 ===")
print(resposta.content)
print()

# 3. CHAIN COM HISTORICO
# Podemos mandar uma lista de mensagens (historico + nova pergunta)
from langchain_core.messages import HumanMessage, SystemMessage

mensagens = [
    SystemMessage(content="Voce e um professor de programacao que explica tudo de forma simples."),
    HumanMessage(content="O que e uma LLM?")
]

resposta2 = modelo.invoke(mensagens)
print("=== RESPOSTA 2 (com SystemMessage) ===")
print(resposta2.content)
print()

# 4. TEMPERATURE TEST
# Temperature baixa = respostas mais previsiveis
# Temperature alta = respostas mais criativas
modelo_frio = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)

print("=== TEMPERATURE 0.0 (sempre a mesma resposta) ===")
for i in range(3):
    r = modelo_frio.invoke("Digite o numero 42")
    print(f"  Tentativa {i+1}: {r.content}")

print()
print("=== TEMPERATURE 0.7 (pode variar) ===")
for i in range(3):
    r = modelo.invoke("Digite o numero 42")
    print(f"  Tentativa {i+1}: {r.content}")
