#%%
# TODO: Add image input

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools import tools
from prompts import sys_prompt
import datetime
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class LLMConversation:
    def __init__(self, provider=os.getenv("DEFAULT_PROVIDER")):
        self.provider = provider.lower()
        self.llm = self._initialize_llm()
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.messages = [SystemMessage(content=sys_prompt.format(user_name=os.getenv("USER_NAME"), date=datetime.datetime.now().strftime("%Y-%m-%d")))]

    def _initialize_llm(self):
        if self.provider == "openai":
            return ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"))
        elif self.provider == "anthropic":
            return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL_NAME"))
        elif self.provider == "google":
            return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL_NAME"))
        elif self.provider == "azure":
            return AzureChatOpenAI(
                azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

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
# conversation = LLMConversation(provider="openai")
# conversation.add_message("Hello, how are you?")
# response = conversation.call_llm()
# print(response)

# Tests for each provider

# test_input = "what is 32 time 41 then take the result and subtract 256"

# providers = ["openai", "anthropic", "azure", "google"]

# for provider in providers:
#     try:
#         print(f"\nTesting {provider.capitalize()} provider:")
#         conversation = LLMConversation(provider=provider)
#         conversation.add_message(test_input)
#         response = conversation.call_llm()
#         print(f"Input: {test_input}")
#         print(f"Response: {response}")
#     except Exception as e:
#         print(f"Error testing {provider} provider: {str(e)}")

# %%
