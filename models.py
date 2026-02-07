import os
from dotenv import load_dotenv
from schemas import json_schema

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model

main_agent = create_agent(
    model = "gpt-5-nano",
    tools=[],
    middleware=[],
    response_format=ToolStrategy(json_schema)
)

summary_model = init_chat_model(
    "gpt-4",
    temperature = 0.0
)
