from langchain_core.tools import wrap_tool_call


@wrap_tool_call
def process_tool_output(result):
    # type controll
    if isinstance(result, str):

        result = result.strip()
        result = result[:300]

    return result
