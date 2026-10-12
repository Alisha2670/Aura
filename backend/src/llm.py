import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

# Load environment variables from .env file
load_dotenv()

def get_llm(temperature: float = 0.0, model_name: str | None = None) -> BaseChatModel:
    """
    Factory function to initialize and return an LLM instance.
    Supports Groq, Google Gemini, and OpenAI.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if groq_key and groq_key.strip() and groq_key != "your_groq_api_key_here":
        from langchain_groq import ChatGroq
        selected_model = model_name or "openai/gpt-oss-20b"
        return ChatGroq(
            model=selected_model,
            temperature=temperature,
            groq_api_key=groq_key
        )
    elif gemini_key and gemini_key.strip() and gemini_key != "your_gemini_api_key_here":
        from langchain_google_genai import ChatGoogleGenerativeAI
        selected_model = model_name or "gemini-2.5-flash"
        return ChatGoogleGenerativeAI(
            model=selected_model,
            temperature=temperature,
            google_api_key=gemini_key
        )
    elif openai_key and openai_key.strip() and openai_key != "your_openai_api_key_here":
        from langchain_openai import ChatOpenAI
        selected_model = model_name or "gpt-4o-mini"
        return ChatOpenAI(
            model=selected_model,
            temperature=temperature,
            api_key=openai_key
        )
    else:
        raise ValueError(
            "No valid API key found. Please set GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in your .env file."
        )
