#%%
from nlp.llm_interface import LLMConversation
from utils.img_to_base import image_to_base64
from utils.config import logger

img = image_to_base64("/home/pi/ai_assistant/test_files/sunny-beach.png")

# Initialize the conversation
conversation = LLMConversation()

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the conversation.", flush=True)
        break
    conversation.add_message(user_input)
    response = conversation.call_llm()
    print("LLM: ", response, flush=True)




"""
# Round 1: Ask about an image
conversation.add_message("What is in this image?", img)
response = conversation.call_llm()
print("LLM Response to Image Question:", response)

# Round 2: Follow-up question
conversation.add_message("Can you describe the colors in the image?")
response = conversation.call_llm()
print("LLM Response to Color Question:", response)

# Round 3: Another follow-up question
conversation.add_message("What objects can you identify in the image?")
response = conversation.call_llm()
print("LLM Response to Objects Question:", response)

# Round 4: Ask about the conversation history
conversation.add_message("Have I asked you anything before this?")
response = conversation.call_llm()
print("LLM Response to History Question:", response)

print("-"*100)

conversation = LLMConversation()

conversation.add_message("what is 32 plus 63, then take the result and multiply it by 3?")
response = conversation.call_llm()
print(response)

conversation.add_message("now add 12 to the result")
response = conversation.call_llm()
print(response)
"""

# %%
