import os
import openai
from dotenv import load_dotenv

def AI_Response(text:str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=100,
        temperature=0
    )
    return response
