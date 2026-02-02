import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
model = init_chat_model("gpt-5-nano")


