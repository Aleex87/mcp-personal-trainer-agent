import asyncio
import re

from src.agent.agent import build_agent
from src.agent.memory import ConversationMemory

from util.pretty_print import print_welcome, get_user_input
from util.streaming_utils import STREAM_MODES, handle_stream_async


def extract_user_info(messages):
    text = " ".join([m["content"].lower() for m in messages])

    data = {
        "age": None,
        "weight": None,
        "height": None,
        "gender": None,
        "level": None,
    }

    # numbers
    numbers = [int(n) for n in re.findall(r"\b\d+\b", text)]

    for n in numbers:
        if 10 < n < 100 and data["age"] is None:
            data["age"] = n
        elif 40 < n < 200 and data["weight"] is None:
            data["weight"] = n
        elif 100 < n < 250 and data["height"] is None:
            data["height"] = n
    # gender
    if any(g in text for g in ["male", "man"]):
        data["gender"] = "male"
    elif any(g in text for g in ["female", "woman"]):
        data["gender"] = "female"
    # level 
    if "beginner" in text:
        data["level"] = "beginner"
    elif "intermediate" in text:
        data["level"] = "intermediate"
    elif "advanced" in text:
        data["level"] = "advanced"

    return data


def is_complete(data):
    return all(data.values())


async def run_async():
    print_welcome(
        title="Personal Trainer Agent",
        description="Agent connected to MCP server with tool usage",
    )

    print("Type 'exit' to quit or 'refresh' to reset memory.\n")

    agent = await build_agent()

    memory = ConversationMemory(max_messages=20)

    while True:
        user_input = get_user_input("Ask something")

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower() == "refresh":
            memory.clear()
            print("Memory cleared.\n")
            continue

        messages = memory.get_recent_messages(4) + [
            {"role": "user", "content": user_input}
        ]

        user_data = extract_user_info(messages)

        if not is_complete(user_data):
            print("\nTrainer Agent:")
            print("I need some more details before creating your plan.\n")

            if not user_data["age"]:
                print("- Age")
            if not user_data["weight"]:
                print("- Weight")
            if not user_data["height"]:
                print("- Height")
            if not user_data["gender"]:
                print("- Gender")
            if not user_data["level"]:
                print("- Fitness level")

            print("\nExample: 30 years old, 80 kg, 180 cm, male, beginner\n")

            memory.add_user_message(user_input)
            continue

        process_stream = agent.astream(
            {"messages": messages},
            stream_mode=STREAM_MODES,
        )

        final_response = await handle_stream_async(
            process_stream,
            agent_name="Trainer Agent",
        )

        memory.add_user_message(user_input)
        memory.add_assistant_message(final_response)


def run():
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
