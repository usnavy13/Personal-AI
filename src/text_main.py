#%%
#%%
from nlp.llm_interface import LLMConversation
from utils.config import logger
from dotenv import load_dotenv

load_dotenv()

# Removed ACTIVATION_WORD and CONVERSATION_ACTIVE

def get_text_input():
    return input("Enter your message (or press Enter to end the conversation): ")

conversation = LLMConversation()

while True:
    user_input = get_text_input()
    
    if user_input:
        conversation.add_message(user_input)
        response = conversation.call_llm()
        print("LLM: ", response)
    else:
        print("No input detected. Exiting...")
        break