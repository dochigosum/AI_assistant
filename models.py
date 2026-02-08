import os
from dotenv import load_dotenv
from schemas import json_schema

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.chat_models import init_chat_model


summary_model = init_chat_model(
    "gpt-5-nano",
    temperature = 0.0
)

learning_guardrail_model = init_chat_model(
    "gpt-5-nano",
    temperature = 0.0,
)

negative_guardrail_model = init_chat_model(
    "gpt-5-nano",
    temperature = 0.0,
)


from schemas import NegativeGuardrail,LearningGuardrail
structured_negative_guardrail_model = learning_guardrail_model.with_structured_output(NegativeGuardrail)
structured_learning_guardrail_model = learning_guardrail_model.with_structured_output(LearningGuardrail)

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from middelware import my_guardrail_middleware

main_agent = create_agent(
    model = "gpt-5-mini",
    tools=[],
    middleware=[my_guardrail_middleware],
    response_format=ToolStrategy(json_schema)
)
