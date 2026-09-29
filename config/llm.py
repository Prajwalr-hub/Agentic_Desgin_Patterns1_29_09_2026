from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def get_llm(temp=0):
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temp
    )