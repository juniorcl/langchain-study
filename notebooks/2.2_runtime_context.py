import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    from dataclasses import dataclass

    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langchain_ollama.chat_models import ChatOllama

    return ChatOllama, HumanMessage, ToolRuntime, create_agent, dataclass, tool


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Functions
    """)
    return


@app.cell
def _(ToolRuntime, dataclass, tool):
    @dataclass
    class ColourContext:
        favourite_colour: str = "blue"
        least_favourite_colour: str = "yellow"

    # o context é passado por meio de funções que recebem um objeto chamado runtime
    @tool
    def get_favourite_colour(runtime: ToolRuntime) -> str:
        """Get the favourite colour of the user"""
        return runtime.context.favourite_colour

    @tool
    def get_least_favourite_colour(runtime: ToolRuntime) -> str:
        """Get the least favourite colour of the user"""
        return runtime.context.least_favourite_colour

    return ColourContext, get_favourite_colour, get_least_favourite_colour


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Acessing the Context
    """)
    return


@app.cell
def _(ChatOllama, ColourContext, create_agent):
    llm = ChatOllama(model='qwen2.5:7b')
    agent = create_agent(model=llm, context_schema=ColourContext)
    return agent, llm


@app.cell
def _(ColourContext, HumanMessage, agent):
    response = agent.invoke(
        {"messages": [HumanMessage(content="What is my favourite colour?")]},
        context=ColourContext()
    )
    return (response,)


@app.cell
def _(response):
    response
    return


@app.cell
def _(
    ColourContext,
    create_agent,
    get_favourite_colour,
    get_least_favourite_colour,
    llm,
):
    agent_context = create_agent(model=llm, context_schema=ColourContext, tools=[get_favourite_colour, get_least_favourite_colour])
    return (agent_context,)


@app.cell
def _(ColourContext, HumanMessage, agent_context):
    response_context = agent_context.invoke(
        {"messages": [HumanMessage(content="What is my favourite colour?")]},
        context=ColourContext()
    )
    return (response_context,)


@app.cell
def _(response_context):
    response_context
    return


@app.cell
def _(ColourContext, HumanMessage, agent_context):
    response_context2 = agent_context.invoke(
        {"messages": [HumanMessage(content="What is my favourite colour?")]},
        context=ColourContext(favourite_colour="green")
    )
    return (response_context2,)


@app.cell
def _(response_context2):
    response_context2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    No LangChain, o **contexto serve para fornecer aos Grandes Modelos de Linguagem (LLMs) as informações externas, históricas ou relevantes necessárias para realizar tarefas de forma precisa, superando as limitações do conhecimento base do modelo**. Ele transforma modelos generalistas em ferramentas especializadas para dados específicos, um processo conhecido como "engenharia de contexto" (*context engineering*).
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
