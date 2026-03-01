import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    from langchain.agents import create_agent
    from langchain.chat_models import init_chat_model
    from langchain_ollama import ChatOllama
    from langchain.messages import HumanMessage, AIMessage

    return AIMessage, ChatOllama, HumanMessage, create_agent, init_chat_model


@app.cell
def _(mo):
    mo.md(r"""
    # Iniciando e Invocando o Modelo
    """)
    return


@app.cell
def _(ChatOllama):
    llm = ChatOllama(model='llama3.2:3b', temperature=0)
    response = llm.invoke("Do you understand portuguese?")
    return llm, response


@app.cell
def _(response):
    print(response.content)
    return


@app.cell
def _(init_chat_model):
    model2 = init_chat_model(model='llama3.2:3b', model_provider='ollama')
    response2 = model2.invoke("Me explique overfitting")
    return (response2,)


@app.cell
def _(response2):
    print(response2.content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Customizando o Modelo
    """)
    return


@app.cell
def _(init_chat_model):
    model3 = init_chat_model(
        model='llama3.2:3b', model_provider='ollama', temperature=1.0)
    response3 = model3.invoke("O que é overfitting?")
    return (response3,)


@app.cell
def _(response3):
    print(response3.content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Iniciando e Invocando uma Agente
    """)
    return


@app.cell
def _(create_agent, llm):
    agent = create_agent(model=llm)
    return (agent,)


@app.cell
def _(HumanMessage, agent):
    response4 = agent.invoke(
        {"messages": [HumanMessage(content="What's the capital of the Moon?")]}
    )
    return (response4,)


@app.cell
def _(response4):
    response4
    return


@app.cell
def _(response4):
    print(response4['messages'][-1].content)
    return


@app.cell
def _(AIMessage, HumanMessage, agent):
    response5 = agent.invoke(
        {
            "messages": [
                HumanMessage(content="What's the capital of the Moon?"),
                AIMessage("The Capital of the Moon is Luna City"),
                HumanMessage("Interesting, tell me more about Luna City")
            ]
        }
    )
    return (response5,)


@app.cell
def _(response5):
    response5
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Streaming Output
    """)
    return


@app.cell
def _(HumanMessage, agent):
    stream = agent.stream(
        {"messages": [HumanMessage(content="Tell me all about Luna City, the capital of the Moon")]},
        stream_mode="messages"
    )

    for token, metadata in stream:
        # token is a message chunk with token content
        # metadata contains which node produced the token
    
        if token.content:  # Check if there's actual content
            print(token.content, end="", flush=True)  # Print token
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
