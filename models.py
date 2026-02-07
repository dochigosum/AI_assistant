import os
from dotenv import load_dotenv
from schemas import json_schema

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model = "gpt-5-nano",
    tools=[],
    response_format=ToolStrategy(json_schema)
)
