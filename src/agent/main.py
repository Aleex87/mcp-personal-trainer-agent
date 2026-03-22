import asyncio

from agent.agent import build_agent

async def run_async():
    print("Starting Personal Trainer Agent ...\n")

    agent = await build_agent()

    while True:
        user_input = input( "Ask something ( or 'exit'):").strip()

        if user_input.lower() == "exit":
            print("Goodby...!")
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
    