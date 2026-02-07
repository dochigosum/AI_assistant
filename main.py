from models import agent
from prompts import sys_prompt
import json

sys_message = {'role':'system','content':sys_prompt}

user_input = input()
structured_user_input = {'role':'user','content':user_input}

with open('test.json', 'r', encoding='utf-8') as f:
    history = json.load(f)
history = history['messages']

print('시작')
response = agent.invoke(
    {'messages':[sys_message]+history+[structured_user_input]}
)
print('끝')

print(response['structured_response'])

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump({'messages':history+[structured_user_input,response['structured_response']]}, f, ensure_ascii=False, indent=2)
