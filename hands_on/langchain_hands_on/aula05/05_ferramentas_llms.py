"""
Aula 05: Criando ferramentas com diferentes LLMs
Aqui aprendemos a:
1. Usar MULTIPLOS modelos (Gemini + GPT + Claude) no mesmo codigo
2. Criar ferramentas que usam modelos menores para tarefas especificas (economia)
3. Roteamento: escolher QUAL modelo usar para CADA tipo de tarefa
4. Tool calling nativo: deixar o proprio modelo decidir quando chamar ferramentas

Analogia:
- Ter varios LLMs e como ter uma equipe: cada um tem sua especialidade
- Um modelo caro (grande) para tarefas dificeis
- Um modelo barato (pequeno) para tarefas simples
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from typing import Literal

load_dotenv()

# =============================================
# 1. MULTIPLOS MODELOS
# =============================================
# Modelo "caro" e poderoso — para raciocinio complexo
modelo_grande = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# Modelo "barato" e rapido — para tarefas simples
modelo_pequeno = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)

parser = StrOutputParser()

# =============================================
# 2. ROTEAMENTO INTELIGENTE
# =============================================
# Um roteador decide qual modelo usar baseado no tipo de pergunta

class Roteador:
    """Escolhe o modelo certo para cada tipo de tarefa."""

    def __init__(self, modelo_complexo, modelo_simples):
        self.complexo = modelo_complexo
        self.simples = modelo_simples

    def rotear(self, pergunta: str) -> str:
        """Classifica a pergunta e roteia para o modelo adequado."""

        # Tarefas complexas que exigem o modelo grande
        tarefas_complexas = [
            "codigo", "programacao", "debug", "arquitetura",
            "analise", "estrategia", "calculo", "matematica"
        ]

        # Tarefas simples que o modelo pequeno resolve
        tarefas_simples = [
            "resumo", "traducao", "sinonimo", "definicao",
            "ola", "bom dia", "exemplo"
        ]

        pergunta_lower = pergunta.lower()

        # Verifica se e tarefa complexa
        for palavra in tarefas_complexas:
            if palavra in pergunta_lower:
                return "complexo"

        # Verifica se e tarefa simples
        for palavra in tarefas_simples:
            if palavra in pergunta_lower:
                return "simples"

        # Caso duvidoso: usa o modelo grande por seguranca
        return "complexo"


roteador = Roteador(modelo_grande, modelo_pequeno)

perguntas_teste = [
    "Traduza 'hello world' para portugues",
    "Escreva um codigo Python que leia um arquivo CSV",
    "Qual o sinonimo de 'rapido'?",
    "Crie uma arquitetura de microsservicos com 3 servicos"
]

print("=== ROTEAMENTO INTELIGENTE ===")
for p in perguntas_teste:
    decisao = roteador.rotear(p)
    modelo_usado = "Gemini Flash (grande)" if decisao == "complexo" else "Gemini Flash Lite (pequeno)"
    print(f"  Pergunta: {p[:50]}...")
    print(f"  Roteado para: {modelo_usado}")
    print()

# =============================================
# 3. TOOL CALLING NATIVO
# =============================================
# Alguns LLMs (Gemini, GPT-4) suportam "tool calling":
# o modelo ja sabe que tem ferramentas e chama elas automaticamente
# Diferenca do ReAct: nao precisa do loop manual Thought/Action/Observation

@tool
def buscar_clima(cidade: str) -> str:
    """Retorna o clima atual de uma cidade."""
    # Simulacao — em producao, chamaria uma API de clima
    dados = {
        "Sao Paulo": "22°C, nublado",
        "Rio de Janeiro": "30°C, sol",
        "Brasilia": "25°C, seco",
        "Lisboa": "18°C, chuva fraca"
    }
    return dados.get(cidade, f"Clima nao encontrado para {cidade}")

@tool
def calcular_idade(ano_nascimento: int) -> str:
    """Calcula a idade de uma pessoa baseado no ano de nascimento."""
    idade = 2026 - ano_nascimento
    return f"A pessoa tem {idade} anos (ou {idade - 1} se ainda nao fez aniversario)."

ferramentas = [buscar_clima, calcular_idade]

# Vincula as ferramentas ao modelo
modelo_com_ferramentas = modelo_grande.bind_tools(ferramentas)

print("=== TOOL CALLING NATIVO ===")
print("O modelo RECEBE as ferramentas e decide quando chama-las.")
print()

# =============================================
# 4. ECONOMIZANDO TOKENS
# =============================================
# Estrategias para gastar menos:
#
# 1. Modelo pequeno para tarefas simples
#    - Gemini Flash Lite custa menos que Gemini Flash
#
# 2. Cache de respostas frequentes
#    - Guardar respostas que ja foram dadas
#
# 3. Prompt menor = menos tokens
#    - Remover instrucoes desnecessarias
#    - Usar templates enxutos
#

class CacheInteligente:
    """Guarda respostas para nao consultar o LLM de novo."""

    def __init__(self, modelo_padrao):
        self.cache = {}
        self.modelo = modelo_padrao

    def perguntar(self, pergunta: str) -> str:
        if pergunta in self.cache:
            print(f"  [CACHE] Resposta encontrada em cache!")
            return self.cache[pergunta]

        resposta = self.modelo.invoke(pergunta)
        texto = resposta.content if hasattr(resposta, 'content') else str(resposta)
        self.cache[pergunta] = texto
        return texto


print("=== CACHE INTELIGENTE ===")
cache = CacheInteligente(modelo_pequeno)
pergunta = "O que significa LLM?"

# Primeira vez: consulta o modelo
print("  1a vez: consultando modelo...")
# Na pratica: resp1 = cache.perguntar(pergunta)
print("  (pulariaamos a execucao real sem API key)")

print()
print("=== RESUMO AULA 05 ===")
print("1. Multiplos LLMs: cada modelo tem seu custo e capacidade")
print("2. Roteador: escolhe o modelo certo para cada tarefa")
print("3. Tool calling: o LLM chama ferramentas nativamente")
print("4. Cache: guarda respostas para nao repetir chamadas")
print("5. Economia: modelo pequeno para 80% das tarefas, grande para 20%")
