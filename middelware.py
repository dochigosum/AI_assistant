from langchain.agents.middleware import before_agent
from models import structured_learning_guardrail_model
from prompts import learning_guardrail_prompt

@before_agent(can_jump_to=["end"])
def my_guardrail_middleware(state, runtime) :
    if not state["messages"]: return None
    last_message = state["messages"][-1]
    if last_message.type != "human": return None

    user_text = last_message.content
    response = structured_learning_guardrail_model.invoke(
        [{"role": "system", "content": f"{learning_guardrail_prompt}"}] + [ {"role": "user", "content": user_text}]
    )

    if not response.is_corrected:
        return {
            "structured_response": {
                "role": "guardrail",
                "content": "능딸",
            },
            "jump_to": "end"
        }

    return None

