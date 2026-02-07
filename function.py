from prompts import summary_prompt
from models import summary_model

def summarization(memory : list, trigger : int = 16, keep : int = 2, system_prompt : str = summary_prompt) :
    if len(memory) >= trigger:
        response = summary_model.invoke(
            [{"role": "system", "content": f"{system_prompt}"}] + memory[:-keep] + [
                {"role": "user", "content": f"지금까지 나눈 대화를 요약해줘"}]
        )
        return [{'role':'user','content':response.content}]
    else:
        return memory