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
    from dotenv import load_dotenv

    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langchain_ollama.chat_models import ChatOllama
    from langchain_mcp_adapters.client import MultiServerMCPClient

    return ChatOllama, HumanMessage, MultiServerMCPClient, create_agent


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # O que é um MCP?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **MCP fornece uma "linguagem" segura e padronizada para que LLMs se comuniquem com dados, aplicativos e serviços externos**. Ele atua como uma ponte, permitindo que a IA vá além do conhecimento estático e se torne um agente dinâmico que pode recuperar informações atuais e agir, tornando-a mais precisa, útil e automatizada.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Online MCP Server
    """)
    return


@app.cell
async def _(MultiServerMCPClient):
    client = MultiServerMCPClient(
        {
            "time": {
                "transport": "stdio",
                "command": "uvx",
                "args": [
                    "mcp-server-time",
                    "--local-timezone=America/Sao_Paulo"
                ]
            }
        }
    )

    tools = await client.get_tools()
    return (tools,)


@app.cell
def _(ChatOllama, create_agent, tools):
    llm = ChatOllama(model='qwen2.5:7b')
    agent = create_agent(model=llm, tools=tools)
    return (agent,)


@app.cell
async def _(HumanMessage, agent):
    question = HumanMessage(content="Qual o horário oficial do estado da cidade de Paraty no Rio de Janeiro?")

    response = await agent.ainvoke({"messages": [question]})
    return (response,)


@app.cell
def _(response):
    response
    return


@app.cell
def _(response):
    print(response["messages"][-1].content)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
