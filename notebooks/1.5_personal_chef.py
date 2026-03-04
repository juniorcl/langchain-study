import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    import marimo as mo

    from typing import Any
    from dotenv import load_dotenv
    from tavily import TavilyClient

    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langchain_ollama.chat_models import ChatOllama

    from langgraph.checkpoint.memory import InMemorySaver

    return (
        Any,
        ChatOllama,
        HumanMessage,
        InMemorySaver,
        TavilyClient,
        create_agent,
        load_dotenv,
        mo,
        tool,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The Chief Agent
    """)
    return


@app.cell
def _(load_dotenv):
    load_dotenv()
    return


@app.cell
def _(TavilyClient):
    tavily_client = TavilyClient()
    return (tavily_client,)


@app.cell
def _(Any, tavily_client, tool):
    @tool
    def web_search(query: str) -> dict[str | Any]:
        """
        Search the web for information

        Args:
            query: The information to search from the web (str).

        Return:
            The information from the web search (dict[str | Any])
        """

        return tavily_client.search(query)

    return (web_search,)


@app.cell
def _():
    system_prompt = """
    You are a personal chef. The user will give you a list of ingredients they have left over in their house.

    Using the web search tool, search the web for recipes that can be made with the ingredients they have.

    Return recipe suggestions and eventually the recipe instructions to the user, if requested.
    """
    return (system_prompt,)


@app.cell
def _(ChatOllama):
    llm = ChatOllama(model='qwen2.5:7b')
    return (llm,)


@app.cell
def _(InMemorySaver, create_agent, llm, system_prompt, web_search):
    agent = create_agent(
        llm,
        tools=[web_search],
        system_prompt=system_prompt,
        checkpointer=InMemorySaver()
    )
    return (agent,)


@app.cell
def _(HumanMessage, agent):
    config = {"configurable": {"thread_id": "1"}}

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content="I have some leftover chicken and rice. What can I make?")
            ]
        },
        config
    )
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
def _():
    return


if __name__ == "__main__":
    app.run()
