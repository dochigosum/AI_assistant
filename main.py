from models import main_agent
from prompts import sys_prompt
from function import summarization, get_memory, send_memory


sys_message = {'role':'system','content':sys_prompt}

user_input = input()
structured_user_input = {'role':'user','content':user_input}

history = get_memory('test.json')

history = summarization(history,trigger=20)

response = main_agent.invoke(
    {'messages':[sys_message]+history+[structured_user_input]}
)

print(response['structured_response'])

send_memory(
    filename='test.json',
    history=history,
    user_message=structured_user_input,
    message=response['structured_response']
)


