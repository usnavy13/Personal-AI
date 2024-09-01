#%%
# TODO: Add image input

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools import tools

def call_llm(query: str) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools)

    messages = [HumanMessage(content=query)]

    while True:
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            break

        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = next((tool for tool in tools if tool.name.lower() == tool_name), None)
            if selected_tool:
                tool_msg = selected_tool.invoke(tool_call)
                messages.append(tool_msg)
            else:
                print(f"Warning: Tool '{tool_name}' not found")

    return ai_msg.content

# Example usage
result = call_llm("What is 3 * 12? then subtract 22 from the result")
print(result)

# %%
