from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from util.models import get_model
from util.pretty_print import print_mcp_tools

from src.agent.prompt import SYSTEM_PROMPT
from src.agent.tool_filter import filter_tools


async def build_agent():
    model = get_model()

    mcp_client = MultiServerMCPClient(
        {
            "trainer_server": {
                "transport": "streamable_http",
                "url": "http://localhost:8001/mcp",
            }
        }
    )

    tools = await mcp_client.get_tools()
    print_mcp_tools(tools, server_name="trainer_server")

    filtered_tools = filter_tools(tools)

    print("\nFiltered tools:")
    for tool in filtered_tools:
        print(f"- {tool.name}")

    agent = create_agent(
        model=model,
        tools=filtered_tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent
