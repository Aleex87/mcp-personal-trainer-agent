from langchain_core.tools import StructuredTool


def process_tool_output(tool):

    def safe_func(**kwargs):
        result = tool.invoke(kwargs)

        if isinstance(result, str):
            result = result.strip()
            result = result[:300]

        return result

    async def safe_func_async(**kwargs):
        result = await tool.ainvoke(kwargs)

        if isinstance(result, str):
            result = result.strip()
            result = result[:300]

        return result

    return StructuredTool.from_function(
        func=safe_func,
        coroutine=safe_func_async,
        name=tool.name,
        description=tool.description,
    )
