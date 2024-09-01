#%%
# TODO: Add image input

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .tools import tools
from .prompts import sys_prompt
import datetime
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class LLMConversation:
    def __init__(self, model="gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model)
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.messages = [SystemMessage(content=sys_prompt.format(user_name=os.getenv("USER_NAME"), date=datetime.datetime.now().strftime("%Y-%m-%d")))]

    def add_message(self, content: str, image: str = 'No Image'):
        if image != 'No Image':
            self.messages.append(HumanMessage(content=[
                {"type": "text", "text": content},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}},
            ]))
        else:
            self.messages.append(HumanMessage(content=content))

    def call_llm(self) -> str:
        while True:
            ai_msg = self.llm_with_tools.invoke(self.messages)
            self.messages.append(ai_msg)

            if not ai_msg.tool_calls:
                break

            for tool_call in ai_msg.tool_calls:
                tool_name = tool_call["name"].lower()
                selected_tool = next((tool for tool in tools if tool.name.lower() == tool_name), None)
                if selected_tool:
                    tool_msg = selected_tool.invoke(tool_call)
                    self.messages.append(tool_msg)
                else:
                    logger.warning(f"Warning: Tool '{tool_name}' not found")

        return ai_msg.content

# Example usage
# conversation = LLMConversation()
# conversation.add_message("Hello, how are you?")
# response = conversation.call_llm()
# print(response)

# %%
