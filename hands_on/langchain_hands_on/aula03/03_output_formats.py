"""
Aula 03: Estruturando saidas — diferentes formatos de resposta
Aqui aprendemos a receber respostas em formatos especificos:

1. Texto simples (StrOutputParser)
2. Lista (CommaSeparatedListOutputParser)
3. JSON estruturado (JsonOutputParser / PydanticOutputParser)
4. Dicionario com campos especificos (Pydanic)

Utilitario: quando voce query um LLM, ele devolve texto.
Os parsers convertem esse texto em dados que seu codigo pode usar.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    CommaSeparatedListOutputParser,
    JsonOutputParser
)
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

modelo = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)
parser_texto = StrOutputParser()

# =============================================
# 1. SAIDA COMO LISTA
# =============================================
parser_lista = CommaSeparatedListOutputParser()

template_lista = ChatPromptTemplate.from_messages([
    ("system", "Liste 5 {tema}. Responda APENAS como uma lista separada por virgulas, sem numeracao."),
    ("human", "Liste 5 {tema}.")
])

chain_lista = template_lista | modelo | parser_lista

print("=== SAIDA COMO LISTA ===")
lista = chain_lista.invoke({"tema": "frameworks de IA em Python"})
print(lista)
print(f"Tipo: {type(lista)} — {len(lista)} itens")
for i, item in enumerate(lista, 1):
    print(f"  {i}. {item}")
print()

# =============================================
# 2. SAIDA COMO JSON (dicionario)
# =============================================
# JsonOutputParser = extrai um JSON valido do texto
# Perfeito para quando voce quer dados estruturados

parser_json = JsonOutputParser()

template_json = ChatPromptTemplate.from_messages([
    ("system", "Responda no formato JSON com os campos solicitados. Nao use ```."),
    ("human", "Crie um perfil para um profissional de {cargo}. Inclua: nome, senioridade, habilidades (array de 3).")
])

chain_json = template_json | modelo | parser_json

print("=== SAIDA COMO JSON ===")
perfil = chain_json.invoke({"cargo": "AI Engineer"})
print(perfil)
print(f"Tipo: {type(perfil)}")
print(f"Nome: {perfil.get('nome', 'N/A')}")
print(f"Senioridade: {perfil.get('senioridade', 'N/A')}")
print(f"Habilidades: {perfil.get('habilidades', [])}")
print()

# =============================================
# 3. SAIDA COM SCHEMA FIXO (Pydantic)
# =============================================
# Pydantic = define EXATAMENTE a estrutura que voce quer

class Vaga(BaseModel):
    titulo: str = Field(description="Titulo da vaga")
    empresa: str = Field(description="Nome da empresa")
    salario: str = Field(description="Faixa salarial")
    requisitos: list[str] = Field(description="Lista de requisitos")
    remoto: bool = Field(description="Se a vaga e remota")

# Prompt que ja diz o schema esperado
template_vaga = ChatPromptTemplate.from_messages([
    ("system", "Extraia as informacoes da vaga no seguinte formato JSON:\n{schema}"),
    ("human", "{descricao_vaga}")
])

chain_vaga = template_vaga | modelo | JsonOutputParser(pydantic_object=Vaga)

descricao = """
Estamos contratando um AI Solutions Architect!
Empresa: TechFlow AI
Salario: $180k-$220k/ano
Localizacao: Remoto
Requisitos:
- 5+ anos com Python
- Experiencia com LLMs (OpenAI, Claude, Gemini)
- Conhecimento em RAG e agentes
- Docker e cloud (GCP/AWS)
"""

print("=== SAIDA COM SCHEMA FIXO ===")
dados_vaga = chain_vaga.invoke({
    "descricao_vaga": descricao,
    "schema": Vaga.schema_json(indent=2)
})
print(dados_vaga)
print()

# =============================================
# 4. COMPARACAO: TEXTO PURO VS ESTRUTURADO
# =============================================
prompt_livre = ChatPromptTemplate.from_messages([
    ("human", "Descreva o que faz um {cargo} em 3 frases.")
])
chain_livre = prompt_livre | modelo | parser_texto

prompt_json = ChatPromptTemplate.from_messages([
    ("human", 'Descreva o que faz um {cargo}. Responda JSON: {{"resumo": "...", "principais_tarefas": ["..."]}}')
])
chain_json2 = prompt_json | modelo | parser_json

print("=== COMPARACAO: TEXTO VS JSON ===")
texto = chain_livre.invoke({"cargo": "Prompt Engineer"})
print("TEXTO:")
print(texto)
print()
dados = chain_json2.invoke({"cargo": "Prompt Engineer"})
print("JSON:")
print(dados)
