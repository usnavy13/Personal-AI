from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

NAME = os.getenv("ACTIVATION_WORD")
LOCATION = os.getenv("LOCATION")

instructions = f"""
//INSTRUCTIONS: 
Your responses will be translated to audio and spoken to the user. Do not use markdown or formatting. Just plain text.
Do not use abreviations like °F or mph. Instead, use the full word (i.e. degrees fahrenheit, miles per hour).

Your name is {NAME}.
The user is currently located in {LOCATION}
"""

# Instantiation using from_template (recommended)
sys_prompt = PromptTemplate.from_template(("""
                                          Your are a helpful personal assistant for {user_name}. Todays date is {date}.                                          
                                          Always keep your responses short and concise.
                                          """+instructions))
