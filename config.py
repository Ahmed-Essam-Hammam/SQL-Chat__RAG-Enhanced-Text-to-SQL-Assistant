import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")


def get_llm():
    return ChatOpenAI(
        base_url="https://api.cerebras.ai/v1",
        model="gpt-oss-120b",
        api_key=CEREBRAS_API_KEY,
        temperature=0
    )
