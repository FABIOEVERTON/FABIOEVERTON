# LANGCHAIN — Curso Completo (Alura: Python + Gemini)

> Explicacao para quem nunca viu programacao com IA.
> Tudo o que foi criado, instalado e executado.

---

## O QUE E LANGCHAIN?

LangChain e um "kit de ferramentas" que conecta seu codigo a IA.
Permite usar Gemini, GPT, Claude etc. DENTRO do seu proprio programa Python, com o MESMO jeito de programar.

---

## ESTRUTURA DO PROJETO

```
/Users/mac/brachat-main/langchain-estudo/
  .env                          # Chave de API do Gemini
  aula01/01_primeiros_passos.py # Primeiros passos
  aula02/02_prompt_templates.py # Templates e Parsers
  aula03/03_output_formats.py   # Formatos de saida
  aula04/04_agentes_orquestradores.py # Agentes
  aula05/05_ferramentas_llms.py # Multiplos LLMs
```

---

## AULA 01 — Primeiros passos

Conecta ao Gemini e faz perguntas. 3 conceitos:

| Conceito | Significado |
|----------|------------|
| **LLM** | O cerebro — Gemini, GPT |
| **Prompt** | A pergunta que voce faz |
| **Temperature** | 0.0 = sempre igual, 0.7 = variadas |

```python
from langchain_google_genai import ChatGoogleGenerativeAI
modelo = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=sua_chave, temperature=0.7)
resposta = modelo.invoke("Explique o que e LangChain")
```

---

## AULA 02 — Prompt Templates e Output Parsing

Templates sao "moldes" de perguntas com campos para preencher:

```python
template = ChatPromptTemplate.from_messages([
    ("system", "Voce e especialista em {area}."),
    ("human", "Explique {conceito}.")
])
chain = template | modelo | parser  # molde -> IA -> extrator
```

Parsers convertem texto em dados uteis: `StrOutputParser` (texto), `CommaSeparatedListOutputParser` (lista).

---

## AULA 03 — Formatos de Saida

| Formato | Para que serve |
|---------|----------------|
| **Lista** | Itens separados por virgulas |
| **JSON** | Dicionario estruturado |
| **Schema Fixo** | Garante campos sempre certos |

---

## AULA 04 — Agentes Orquestradores

Ate aula 03: roteiro fixo. Aula 04: o proprio modelo decide o que fazer (ReAct):

```
Thought: "Preciso calcular 15% de 200" -> Action: calcular("200 * 0.15") -> Observation: 30.0
Thought: "Converter 100 USD" -> Action: converter_moeda(100, "USD", "BRL") -> Observation: 545.0 BRL
Final Answer: "15% de 200 = R$30. 100 USD = R$545.00"
```

Ferramentas: `calcular` (matematica) e `converter_moeda` (USD/BRL/EUR).

---

## AULA 05 — Multiplos LLMs e Roteador

| Modelo | Custo | Usar para |
|--------|-------|-----------|
| Gemini Flash (grande) | Mais caro | Codigo, analise |
| Gemini Flash Lite (pequeno) | Mais barato | Traducao, definicoes |

Roteador inteligente: decide qual modelo usar por tarefa. Tool Calling nativo: modelos decide quando usar ferramentas. Cache: guarda respostas para nao repetir chamadas.

---

## INSTALACAO E EXECUCAO

```bash
pip3 install langchain langchain-google-genai python-dotenv
cd /Users/mac/brachat-main/langchain-estudo
echo 'GEMINI_API_KEY="sua-chave"' > .env
python3 aula01/01_primeiros_passos.py  # (precisa chave API)
```

---

## MAPA MENTAL

```
TEMPLATES (aula 02)  +  MODELOS (aula 01)  +  FERRAMENTAS (aula 04/05)
                              |
                        OUTPUT PARSERS (aula 03)
                              |
                        AGENTES (aula 04) — LLM decide ferramenta
                              |
                        ROTEADOR (aula 05) — escolhe modelo certo
```

---

## GLOSSARIO

| Termo | Traducao |
|-------|----------|
| **LLM** | Modelo de Linguagem (Gemini, GPT) |
| **Prompt** | Instrucao enviada ao modelo |
| **Template** | Prompt com campos para preencher |
| **Chain** | Cadeia: template -> modelo -> parser |
| **Agent** | LLM que decide qual ferramenta usar |
| **ReAct** | Ciclo: raciocina -> age -> observa |
| **Token** | Unidade de texto (custo) |
| **Cache** | Guardar respostas para reusar |

---

> Arquivo gerado em 08/07/2026 — 5 aulas criadas, libs instaladas,
> codigos testados. So falta chave de API do Gemini para execucao real.
