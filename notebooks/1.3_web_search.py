# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "langchain>=1.2.10",
#     "langchain-ollama>=1.0.1",
#     "marimo>=0.20.2",
#     "python-dotenv>=1.2.2",
#     "pyzmq>=27.1.0",
#     "tavily>=1.1.0",
# ]
# ///

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
    from typing import Any
    from dotenv import load_dotenv
    from tavily import TavilyClient

    from langchain.tools import tool
    from langchain_ollama import ChatOllama
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage

    return (
        Any,
        ChatOllama,
        HumanMessage,
        TavilyClient,
        create_agent,
        load_dotenv,
        tool,
    )


@app.cell
def _(load_dotenv):
    load_dotenv()
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Without Web Search
    """)
    return


@app.cell
def _(ChatOllama, create_agent):
    llm = ChatOllama(model='llama3.2:3b', temperature=0)

    agent = create_agent(model=llm)
    return (agent,)


@app.cell
def _(HumanMessage, agent):
    question = HumanMessage(content="How up to date is your training knowledge?")
    response = agent.invoke({"messages": [question]})
    return (response,)


@app.cell
def _(response):
    response
    return


@app.cell
def _(response):
    print(response['messages'][-1].content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Add Web Search Tool
    """)
    return


@app.cell
def _(TavilyClient):
    tavily_client = TavilyClient()
    return (tavily_client,)


@app.cell
def _(Any, tavily_client, tool):
    @tool
    def web_search(query: str) -> dict[str, Any]:
        """Search the web for information"""
        return tavily_client.search(query)

    return (web_search,)


@app.cell
def _(ChatOllama, HumanMessage, create_agent, web_search):
    llm2 = ChatOllama(model='qwen2.5:7b', temperature=0)

    agent2 = create_agent(model=llm2, tools=[web_search])

    question2 = HumanMessage(content="Use the tool to know the current mayor of Rio de Janeiro?")

    response2 = agent2.invoke({"messages": [question2]})
    return (response2,)


@app.cell
def _(response2):
    response2
    return


@app.cell
def _(response2):
    response2['messages'][-1]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
