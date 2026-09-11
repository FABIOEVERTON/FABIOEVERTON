"""ReAct agent with tool calling capabilities."""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from src.config import get_settings
from src.utils.router import router


@tool
def calculator(expression: str) -> str:
    """Calcula uma expressão matemática.

    Args:
        expression: Expressão matemática para avaliar.

    Returns:
        Resultado do cálculo.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Erro no cálculo: {e}"


@tool
def word_counter(text: str) -> str:
    """Conta palavras e caracteres de um texto.

    Args:
        text: Texto para analisar.

    Returns:
        Estatísticas do texto.
    """
    words = len(text.split())
    chars = len(text)
    sentences = text.count(".") + text.count("!") + text.count("?")
    return f"Palavras: {words}, Caracteres: {chars}, Frases: {sentences}"


@tool
def text_summarizer(text: str) -> str:
    """Gera um resumo conciso do texto.

    Args:
        text: Texto para resumir.

    Returns:
        Resumo do texto.
    """
    sentences = text.split(".")
    summary = ". ".join(s.strip() for s in sentences[:3] if s.strip())
    return summary + "." if summary else text[:200]


class ReActAgent:
    """ReAct agent with reasoning and acting capabilities."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.tools = [calculator, word_counter, text_summarizer]
        self.llm = router.route("general task", task_type="general")

    def create_agent(self) -> AgentExecutor:
        """Create a ReAct agent executor.

        Returns:
            Configured AgentExecutor.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente inteligente que usa ferramentas quando necessário. "
             "Pense passo a passo antes de agir."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, prompt)

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
        )

    def run(self, query: str) -> str:
        """Execute the agent with a query.

        Args:
            query: User query.

        Returns:
            Agent response.
        """
        executor = self.create_agent()
        result = executor.invoke({"input": query})
        return result.get("output", "No response")


react_agent = ReActAgent()
