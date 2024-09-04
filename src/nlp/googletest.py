#%%
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

def test_google_provider():
    try:
        # Initialize VertexAI
        llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL_NAME"))

        # Create a simple conversation
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content="Hello, can you tell me a short joke?")
        ]

        # Invoke the model
        response = llm.invoke(messages)

        print("Google VertexAI Test:")
        print(f"Input: {messages[-1].content}")
        print(f"Response: {response.content}")

    except Exception as e:
        print(f"Error testing Google VertexAI provider: {str(e)}")

if __name__ == "__main__":
    test_google_provider()
# %%
