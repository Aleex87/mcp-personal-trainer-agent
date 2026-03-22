from langchain_core.tools import wrap_tool_call
# get the result from the tool,
# controll type take away extra space and set a limit of 300

@wrap_tool_call
def process_tool_output(result):
    # type controll
    if isinstance(result, str):

        result = result.strip()
        result = result[:300]

    return result
