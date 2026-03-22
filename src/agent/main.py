import asyncio

from agent.agent import build_agent
from util.pretty_print import print_welcome, get_user_input


async def run_async():
    print_welcome(
        title="Personal Trainer Agent",
        description="Agent connected to MCP server with tool usage",
    )

    agent = await build_agent()

    while True:
        user_input = get_user_input("Ask something")

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            }
        )

        print("\nResponse:")
        print(result["messages"][-1].content)
        print("\n" + "-" * 50)


def run():
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
    