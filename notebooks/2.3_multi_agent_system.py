import marimo

__generated_with = "0.20.4"
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

    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langchain_ollama.chat_models import ChatOllama

    return ChatOllama, HumanMessage, create_agent, tool


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Functions
    """)
    return


@app.cell
def _(tool):
    @tool
    def square_root(x: float) -> float:
        """Calculate the square root of a number"""
        return x ** 0.5

    @tool
    def square(x: float) -> float:
        """Calculate the square of a number"""
        return x ** 2

    return square, square_root


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Creating Subagent
    """)
    return


@app.cell
def _(ChatOllama):
    llm = ChatOllama(model='qwen2.5:7b-instruct')
    return (llm,)


@app.cell
def _(create_agent, llm, square, square_root):
    subagent_1 = create_agent(
        model=llm,
        tools=[square_root]
    )

    subagent_2 = create_agent(
        model=llm,
        tools=[square]
    )
    return subagent_1, subagent_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Calling subagents
    """)
    return


@app.cell
def _(HumanMessage, create_agent, llm, subagent_1, subagent_2, tool):
    @tool
    def call_subagent_1(x: float) -> float:
        """Call subagent 1 in order to calculate the square root of a number"""
        response = subagent_1.invoke({"messages": [HumanMessage(content=f"Calculate the square root of {x}")]})
        return response["messages"][-1].content

    @tool
    def call_subagent_2(x: float) -> float:
        """Call subagent 2 in order to calculate the square of a number"""
        response = subagent_2.invoke({"messages": [HumanMessage(content=f"Calculate the square of {x}")]})
        return response["messages"][-1].content

    ## Creating the main agent

    main_agent = create_agent(
        model=llm,
        tools=[call_subagent_1, call_subagent_2],
        system_prompt="You are a helpful assistant who can call subagents to calculate the square root or square of a number.")
    return (main_agent,)


@app.cell
def _(HumanMessage, main_agent):
    question = "What is the square root of 456?"

    response = main_agent.invoke({"messages": [HumanMessage(content=question)]})
    return (response,)


@app.cell
def _(response):
    response
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
