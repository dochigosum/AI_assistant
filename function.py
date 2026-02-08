import json
from prompts import summary_prompt
from models import summary_model

def summarization(memory : list, trigger : int = 16, keep : int = 2, system_prompt : str = summary_prompt) :
    if len(memory) >= trigger:
        response = summary_model.invoke(
            [{"role": "system", "content": f"{system_prompt}"}] + memory[:-keep] + [{"role": "user", "content": f"지금까지 나눈 대화를 요약해줘"}]
        )
        return [{'role':'user','content':response.content}]
    else:
        return memory

def get_memory(filename : str):
    with open(filename, 'r', encoding='utf-8') as f:
        memory = json.load(f)
    memory = memory['messages']
    return memory

def send_memory(filename : str, history : list, user_message : dict, message : dict) :
    if message['role'] == "ai":
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'messages': history + [user_message, message]}, f,ensure_ascii=False, indent=2)
    return