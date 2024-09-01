from langchain_core.prompts import PromptTemplate

# Instantiation using from_template (recommended)
sys_prompt = PromptTemplate.from_template("""
                                          Your are a helpful personal assistant for {user_name}. Todays date is {date}.                                          
                                          Always keep your responses short and concise.
                                          """)
