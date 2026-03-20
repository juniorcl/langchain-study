import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    from typing import Any
    from tavily import TavilyClient
    from dotenv import load_dotenv
    from datetime import datetime, timedelta

    from langchain.tools import tool, ToolRuntime
    from langchain.agents import AgentState, create_agent
    from langchain.messages import HumanMessage, ToolMessage
    from langchain_ollama.chat_models import ChatOllama
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain_community.utilities import SQLDatabase

    return (
        AgentState,
        Any,
        ChatOllama,
        HumanMessage,
        MultiServerMCPClient,
        SQLDatabase,
        TavilyClient,
        ToolRuntime,
        create_agent,
        datetime,
        load_dotenv,
        timedelta,
        tool,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## Functions
    """)
    return


@app.cell
def _(load_dotenv):
    load_dotenv()
    return


@app.cell
async def _(MultiServerMCPClient):
    client = MultiServerMCPClient(
        {
            "travel_server": {
                    "transport": "streamable_http",
                    "url": "https://mcp.kiwi.com"
                }
        }
    )

    tools = await client.get_tools()
    return (tools,)


@app.cell
def _(Any, TavilyClient, tool):
    tavily_client = TavilyClient()

    @tool
    def web_search(query: str) -> dict[str, Any]:
        """Search the web for information"""
        return tavily_client.search(query)

    return (web_search,)


@app.cell
def _(SQLDatabase, tool):
    db = SQLDatabase.from_uri("sqlite:///../data/Chinook.db")

    @tool
    def query_playlist_db(query: str) -> str:

        """Query the database for playlist information"""

        try:
            return db.run(query)
        except Exception as e:
            return f"Error querying database: {e}"

    return (query_playlist_db,)


@app.cell
def _(AgentState):
    class WeddingState(AgentState):
        origin: str
        destination: str
        guest_count: str
        genre: str

    return (WeddingState,)


@app.cell
def _(mo):
    mo.md(r"""
    # Create Subagents
    """)
    return


@app.cell
def _(ChatOllama):
    llm = ChatOllama(model='qwen2.5:7b-instruct')
    return (llm,)


@app.cell
def _(create_agent, llm, tools):
    # Travel agent
    travel_agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
        You are a travel agent. Search for flights to the desired destination wedding location.
        You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
        - Price (lowest, economy class)
        - Duration (shortest)
        - Date (time of year which you believe is best for a wedding at this location)
        To make things easy, only look for one ticket, one way.
        You may need to make multiple searches to iteratively find the best options.
        You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
        Once you have found the best options, let the user know your shortlist of options.

        IMPORTANT:
        - Use a departure date in the future
        - Today is 2026-03-20
        """
    )
    return (travel_agent,)


@app.cell
def _(create_agent, llm, web_search):
    # Venue agent
    venue_agent = create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a venue specialist. Search for venues in the desired location, and with the desired capacity.
        You are not allowed to ask any more follow up questions, you must find the best venue options based on the following criteria:
        - Price (lowest)
        - Capacity (exact match)
        - Reviews (highest)
        You may need to make multiple searches to iteratively find the best options.
        """
    )
    return (venue_agent,)


@app.cell
def _(create_agent, llm, query_playlist_db):
    # Playlist agent
    playlist_agent = create_agent(
        model=llm,
        tools=[query_playlist_db],
        system_prompt="""
        You are a playlist specialist. Query the sql database and curate the perfect playlist for a wedding given a genre.
        Once you have your playlist, calculate the total duration and cost of the playlist, each song has an associated price.
        If you run into errors when querying the database, try to fix them by making changes to the query.
        Do not come back empty handed, keep trying to query the db until you find a list of songs.
        You may need to make multiple queries to iteratively find the best options.
        """
    )
    return (playlist_agent,)


@app.cell
def _(mo):
    mo.md(r"""
    # Create Agent
    """)
    return


@app.cell
def _(
    HumanMessage,
    ToolRuntime,
    future_date,
    playlist_agent,
    tool,
    travel_agent,
    venue_agent,
):
    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """Travel agent searches for flights to the desired destination wedding location."""
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]
        response = await travel_agent.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"""Find flights from {origin} to {destination}.
                        Use EXACTLY this departure date: {future_date}
                        Format: dd/mm/yyyy
                        Do NOT change it.
                        """
                        )
                    ]
                }
            )
        return response['messages'][-1].content

    @tool
    def search_venues(runtime: ToolRuntime) -> str:
        """Venue agent chooses the best venue for the given location and capacity."""
        destination = runtime.state["destination"]
        capacity = runtime.state["guest_count"]
        query = f"Find wedding venues in {destination} for {capacity} guests"
        response = venue_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].content

    @tool
    def suggest_playlist(runtime: ToolRuntime) -> str:
        """Playlist agent curates the perfect playlist for the given genre."""
        genre = runtime.state["genre"]
        query = f"Find {genre} tracks for wedding playlist"
        response = playlist_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].contentdo

    return search_flights, search_venues, suggest_playlist


@app.cell
def _(datetime, timedelta):
    future_date = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
    return (future_date,)


@app.cell
def _(
    WeddingState,
    create_agent,
    llm,
    search_flights,
    search_venues,
    suggest_playlist,
):
    coordinator = create_agent(
        model=llm,
        tools=[search_flights, search_venues, suggest_playlist],
        state_schema=WeddingState,
        system_prompt="""
        You are a wedding coordinator. Delegate tasks to your specialists for flights, venues and playlists.
        First find all the information you need to update the state. Once that is done you can delegate the tasks.
        Once you have received their answers, coordinate the perfect wedding for me.
        """
    )
    return (coordinator,)


@app.cell
async def _(HumanMessage, coordinator, future_date):
    response = await coordinator.ainvoke({
        "messages": [
            HumanMessage(
                content=f"I'm from London and I'd like a wedding in Paris for 100 guests, jazz-genre on {future_date}"
            )
        ],
        "origin": "London",
        "destination": "Paris",
        "guest_count": 100,
        "genre": "jazz",
        "departure_date": f"{future_date}"
    })
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
