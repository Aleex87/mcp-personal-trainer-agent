import asyncio

from src.agent.agent import build_agent
from util.pretty_print import print_welcome, get_user_input
from util.streaming_utils import STREAM_MODES, handle_stream_async


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

        process_stream = agent.astream(
            {
                "messages": [{"role": "user", "content": user_input}]
            },
            stream_mode=STREAM_MODES,
        )

        await handle_stream_async(process_stream, agent_name="Trainer Agent")


def run():
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
    