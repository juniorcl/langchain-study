import marimo

__generated_with = "0.20.3"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain_ollama import ChatOllama
    from langchain.messages import HumanMessage

    return ChatOllama, HumanMessage, create_agent, tool


@app.cell
def _(mo):
    mo.md(r"""
    # Tool Definition
    """)
    return


@app.cell
def _(tool):
    @tool
    def square_root(x: float) -> float:
        """Calculate the square root of a number"""
        return x ** 0.5

    return


@app.cell
def _(tool):
    @tool("square_root")
    def tool1(x: float) -> float:
        """Calculate the square root of a number"""
        return x ** 0.5

    return (tool1,)


@app.cell
def _(tool):
    @tool("square_root", description="Calculate the square root of a number")
    def tool2(x: float) -> float:
        return x ** 0.5

    return


@app.cell
def _(tool1):
    tool1.invoke({"x": 467})
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Adding Agents
    """)
    return


@app.cell
def _(ChatOllama, create_agent, tool1):
    llm = ChatOllama(model='llama3.2:3b', temperature=0)

    agent = create_agent(
        model=llm,
        tools=[tool1],
        system_prompt="You are an arithmetic wizard. Use your tools to calculate the square root and square of any number."
    )
    return (agent,)


@app.cell
def _(HumanMessage, agent):
    question = HumanMessage(content="What is the square root of 467?")

    response = agent.invoke({"messages": [question]})

    print(response['messages'][-1].content)
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
