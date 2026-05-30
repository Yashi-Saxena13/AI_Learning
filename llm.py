# llm.py — one place to define how we call LLMs in this project. 
from dotenv import load_dotenv 
from litellm import completion 
  
load_dotenv() 
  
PRIMARY = "gemini/gemini-2.5-flash" 
FALLBACK = "groq/llama-3.3-70b-versatile" 
  
def ask(messages, **kwargs): 
    """Single LLM call with automatic Gemini -> Groq fallback.""" 
    response = completion( 
        model=PRIMARY, 
        messages=messages, 
        fallbacks=[FALLBACK],   # tried automatically on any failure 
        num_retries=2,          # retry primary twice before falling back 
        timeout=30,             # seconds 
        **kwargs, 
    ) 
    return response 