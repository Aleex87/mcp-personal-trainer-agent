from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from util.models import get_model
from util.pretty_print import print_mcp_tools

from agent.prompt import SYSTEM_PROMPT
from agent.tool_filter import filter_tools
from agent.middleware import process_tool_output

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
    # get the tools from MCP server
    tools = await mcp_client.get_tools()

    # print the tool
    print_mcp_tools(tools, server_name="trainer_server")
    
    filtered_tools = filter_tools(tools)
    print("\nFiltered tools:")
    
    for t in filtered_tools:
        print(f"- {t.name}")
    
    # apply middleware
    safe_tools = [process_tool_output(tool) for tool in filter_tools]

    # create the agent
    agent = create_agent(
        model= model,
        tools=safe_tools,
        system_prompt=SYSTEM_PROMPT,
    )

    return agent
