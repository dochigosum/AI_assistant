from models import main_agent
from prompts import sys_prompt
import json
from function import summarization

sys_message = {'role':'system','content':sys_prompt}

user_input = input()
structured_user_input = {'role':'user','content':user_input}

with open('test.json', 'r', encoding='utf-8') as f:
    history = json.load(f)
history = history['messages']

history = summarization(history,trigger=20)

response = main_agent.invoke(
    {'messages':[sys_message]+history+[structured_user_input]}
)

print(response['structured_response'])

if response['structured_response']['role'] == "ai":
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump({'messages':history+[structured_user_input,response['structured_response']]}, f, ensure_ascii=False, indent=2)

