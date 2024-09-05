#%%
#%%
from nlp.llm_interface import LLMConversation
from utils.img_to_base import image_to_base64
from utils.config import logger
import os
from dotenv import load_dotenv

load_dotenv()

ACTIVATION_WORD = os.getenv("ACTIVATION_WORD")
CONVERSATION_ACTIVE = False

def get_text_input():
    return input("Enter your message (or press Enter to end the conversation): ")

while True:
    user_input = get_text_input()
    
    if user_input:
        if not CONVERSATION_ACTIVE and ACTIVATION_WORD.lower() in user_input.lower():
            # Activate the conversation
            CONVERSATION_ACTIVE = True
            conversation = LLMConversation()
            conversation.add_message(user_input)
            response = conversation.call_llm()
            print("LLM: ", response)
        elif CONVERSATION_ACTIVE:
            # Continue the active conversation
            conversation.add_message(user_input)
            response = conversation.call_llm()
            print("LLM: ", response)
        else:
            # Ignore input when conversation is not active and activation word is not detected
            print("Activation word not detected. Ignoring input.")
    else:
        # End the conversation when no input is detected
        if CONVERSATION_ACTIVE:
            print("No input detected. Ending conversation.")
            CONVERSATION_ACTIVE = False
        else:
            print("No input detected. Exiting...")
            break