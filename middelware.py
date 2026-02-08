from langchain.agents.middleware import before_agent
from models import structured_learning_guardrail_model
from prompts import learning_guardrail_prompt
from negative_words import negative_word_set

@before_agent(can_jump_to=["end"])
def my_guardrail_middleware(state, runtime) :
    if not state["messages"]: return None
    last_message = state["messages"][-1]
    if last_message.type != "human": return None

    user_text = last_message.content

    for negative_word in negative_word_set:
        if negative_word in user_text:
            return {
                "structured_response": {
                    "role": "guardrail",
                    "content": "욕이 감지되었어. 다시한번 질문해 주실수 있으신가요?",
                },
                "jump_to": "end"
            }

    learning_response = structured_learning_guardrail_model.invoke(
        [{"role": "system", "content": f"{learning_guardrail_prompt}"}] + [ {"role": "user", "content": user_text}]
    )

    if not learning_response.is_corrected:
        return {
            "structured_response": {
                "role": "guardrail",
                "content": "질문하신 내용도 흥미롭지만, 저는 학습을 도와주는 AI라 잘 답변하지 못하겠어요. 다른 질문을 시작할 까요?",
            },
            "jump_to": "end"
        }

    return None

