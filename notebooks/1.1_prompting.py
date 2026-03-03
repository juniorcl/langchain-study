# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.20.3",
#     "pyzmq>=27.1.0",
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
    from langchain.agents import create_agent
    from langchain.messages import HumanMessage
    from langchain_ollama import ChatOllama
    from pydantic import BaseModel

    return BaseModel, ChatOllama, HumanMessage, create_agent


@app.cell
def _(mo):
    mo.md(r"""
    # Basic Prompting
    """)
    return


@app.cell
def _(ChatOllama, HumanMessage, create_agent):
    llm = ChatOllama(model='llama3.2:3b', temperature=0)
    agent = create_agent(model=llm)

    question = HumanMessage(content="What's the capital of the moon?")

    response = agent.invoke({"messages": [question]})
    return llm, question, response


@app.cell
def _(response):
    response
    return


@app.cell
def _(response):
    print(response['messages'][-1].content)
    return


@app.cell
def _(create_agent, llm, question):
    system_prompt = "You are a science fiction writer, create a capital city at the users request."

    scifi_agent = create_agent(
        model=llm, 
        system_prompt=system_prompt
    )

    response2 = scifi_agent.invoke({"messages": [question]})
    return


@app.cell
def _(response):
    print(response['messages'][-1].content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Few-shot Examples
    """)
    return


@app.cell
def _(create_agent, llm, question):
    system_prompt2 = """

    You are a science fiction writer, create a space capital city at the users request.

    User: What is the capital of mars?
    Scifi Writer: Marsialis

    User: What is the capital of Venus?
    Scifi Writer: Venusovia

    """

    scifi_agent2 = create_agent(
        model=llm,
        system_prompt=system_prompt2
    )

    response3 = scifi_agent2.invoke({"messages": [question]})
    return (response3,)


@app.cell
def _(response3):
    response3
    return


@app.cell
def _(response3):
    print(response3['messages'][1].content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Structured Prompts
    """)
    return


@app.cell
def _(create_agent, llm, question):
    system_prompt3 = """

    You are a science fiction writer, create a space capital city at the users request.

    Please keep to the below structure.

    Name: The name of the capital city

    Location: Where it is based

    Vibe: 2-3 words to describe its vibe

    Economy: Main industries

    """

    scifi_agent3 = create_agent(
        model=llm,
        system_prompt=system_prompt3
    )

    response4 = scifi_agent3.invoke({"messages": [question]})
    return (response4,)


@app.cell
def _(response4):
    response4
    return


@app.cell
def _(response4):
    print(response4['messages'][1].content)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Structured Outuput
    """)
    return


@app.cell
def _(BaseModel):
    class CapitalInfo(BaseModel):
        name: str
        location: str

    return (CapitalInfo,)


@app.cell
def _(ChatOllama):
    llm2 = ChatOllama(
        model="ministral-3:3b",
        temperature=0,
        num_predict=20,  # ou max_tokens
    )
    return (llm2,)


@app.cell
def _(CapitalInfo, HumanMessage, create_agent, llm2):
    agent3 = create_agent(
        model=llm2,
        system_prompt="You must answer in 1 short sentence (max 10 words). Only provide the capital name and location.",
        response_format=CapitalInfo
    )

    question2 = HumanMessage(content="What is the capital of The Moon?")

    response5 = agent3.invoke({"messages": [question2]})
    return (response5,)


@app.cell
def _(response5):
    response5
    return


@app.cell
def _(response5):
    response5["structured_response"]
    return


@app.cell
def _(response5):
    response5["structured_response"].name
    return


@app.cell
def _(response5):
    capital_info = response5["structured_response"]

    capital_name = capital_info.name
    capital_location = capital_info.location

    print(f"{capital_name} is a city located at {capital_location}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
