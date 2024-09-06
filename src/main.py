#%%
from nlp.llm_interface import LLMConversation
from utils.img_to_base import image_to_base64
from utils.config import logger
from audio.microphone import listen
from audio.speaker import speak
import os
from dotenv import load_dotenv


load_dotenv()

ACTIVATION_WORD = os.getenv("ACTIVATION_WORD")
CONVERSATION_ACTIVE = False

while True:
    user_input = listen()
    
    if user_input is not None:
        if not CONVERSATION_ACTIVE and ACTIVATION_WORD.lower() in user_input.lower():
            # Activate the conversation
            CONVERSATION_ACTIVE = True
            conversation = LLMConversation()
            conversation.add_message(user_input)
            response = conversation.call_llm()
            print("LLM: ", response, flush=True)
            speak(response)
        elif CONVERSATION_ACTIVE:
            conversation.add_message(user_input)
            response = conversation.call_llm()
            print("LLM: ", response, flush=True)
            speak(response)
        else:
            # Ignore input when conversation is not active and activation word is not detected
            print("Activation word not detected. Ignoring input.")
    else:
        # End the conversation when no input is detected
        if CONVERSATION_ACTIVE:
            print("No input detected. Ending conversation.")
            CONVERSATION_ACTIVE = False
        else:
            print("No input detected. Listening again...")


# %%
