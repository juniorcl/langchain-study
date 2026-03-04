# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "langchain==1.2.10",
#     "langchain-ollama==1.0.1",
#     "langgraph==1.0.10",
#     "marimo>=0.20.4",
#     "pyzmq>=27.1.0",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    import marimo as mo

    from langchain_ollama import ChatOllama

    from langchain.agents import create_agent
    from langchain.messages import HumanMessage

    from langgraph.checkpoint.memory import InMemorySaver

    return ChatOllama, HumanMessage, InMemorySaver, create_agent, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # No Memory
    """)
    return


@app.cell
def _(ChatOllama):
    llm = ChatOllama(model='qwen2.5:7b', temperature=0)
    return (llm,)


@app.cell
def _(create_agent, llm):
    agent = create_agent(llm)
    return (agent,)


@app.cell
def _(HumanMessage, agent):
    question = HumanMessage(content="Hello my name is Sean and my favourite colour is green")

    response = agent.invoke({"messages": [question]})
    return question, response


@app.cell
def _(response):
    response
    return


@app.cell
def _(response):
    print(response['messages'][-1].content)
    return


@app.cell
def _(HumanMessage, agent):
    question2 = HumanMessage(content="What's my favourite colour?")
    response2 = agent.invoke({"messages": [question2]})
    return (response2,)


@app.cell
def _(response2):
    response2
    return


@app.cell
def _(response2):
    print(response2['messages'][-1].content)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Não há memória** no modelo ao se utilizar somente o modelo para realizar as chamadas. Por isso é necessário **utilizar o parâmetro *checkpointer* para conseguir manter memória da conversa**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Memory
    """)
    return


@app.cell
def _(HumanMessage, InMemorySaver, create_agent, llm, question):
    agent_memory = create_agent(llm, checkpointer=InMemorySaver())

    question_memory = HumanMessage(content="Hello my name is Seán and my favourite colour is green")
    config = {"configurable": {"thread_id": "1"}}

    response_memory = agent_memory.invoke({"messages": [question]}, config)
    return agent_memory, config, response_memory


@app.cell
def _(response_memory):
    response_memory
    return


@app.cell
def _(HumanMessage, agent_memory, config):
    question_memory2 = HumanMessage(content="What's my favourite colour?")

    response_memory2 = agent_memory.invoke(
        {"messages": [question_memory2]},
        config,  
    )
    return (response_memory2,)


@app.cell
def _(response_memory2):
    response_memory2
    return


@app.cell
def _(response_memory2):
    response_memory2['messages'][-1].content
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### O que é InMemorySaver?

    O `InMemorySaver` é um *checkpointer* do **LangGraph**.

    No LangGraph, a execução do agente é modelada como um grafo de estados.
    A cada passo da execução, o estado pode ser salvo.

    O *checkpointer* é o componente responsável por:

    * Salvar o estado do grafo;

    * Recuperar o estado anterior;

    * Permitir continuidade entre chamadas.

    > Porém por salvar na memória RAM, não é muito adequando em produção.

    ### O que é `config = {'configurable': {'thread_id': '1'}}`

    No LangGraph, o thread_id funciona como um identificador da conversa / sessão. Ele separa estados diferentes dentro do mesmo checkpointer.

    #### Por que é necessário?

    Imagine que você tenha:

    * Usuário A conversando

    * Usuário B conversando

    Se você não usar `thread_id`, ambos podem compartilhar o mesmo estado.

    Com o `thread_id`, você isola:

    ```python
    thread_id = "user_1"
    thread_id = "user_2"
    ```

    Então cada um tem a sua própria memória.

    > Para um agente em produção, o melhor caminho é utilizar um banco de dados para salvar o estado completo e um banco vetorial para salvar a informação semântica.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
