import json

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from models import main_agent
from prompts import sys_prompt
from function import summarization, get_memory, send_memory

class AiRequest(BaseModel):
    user_id : int
    drawing_id : int
    content : str
@app.get('/api/v1/assistant')
def all_read() -> str:
    history = get_memory('test.json')
    if history['role'] == 'user':
        history = history[1:]
    return json.dumps(history,ensure_ascii=False, indent=2)

@app.post('/api/v1/assistant')
def create_users(request_body : AiRequest) -> str:
    sys_message = {'role':'system','content':sys_prompt}

    structured_user_input = {'role':'user','content':request_body.content}

    history = get_memory('test.json')

    history = summarization(history,trigger=16)

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
    return response['structured_response']['content']


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

