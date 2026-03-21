def filter_tools(tools):
    allowed_tool_names = {
        "generate_workout_plan",
        "get_daily_workout",
        "generate_meal_plan",
    }

    return [tool for tool in tools if tool.name in allowed_tool_names]
