import json

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from models import main_agent
from prompts import sys_prompt
from function import summarization, get_memory, send_memory

class AiRequest(BaseModel):
    id : int
    drawing_id : int
    template_name : str
    content : str
@app.get('/api/v1/assistant/{drawing_id}')
def all_read(drawing_id : int) -> str:
    history = get_memory()
    if history and history[0]['role'] == 'user':
        history = history[1:]
    return json.dumps(history,ensure_ascii=False, indent=2)

@app.post('/api/v1/assistant')
def create_users(request_body : AiRequest) -> str:
    sys_message = {'role':'system','content':sys_prompt}

    structured_user_input = {'role':'user','content':request_body.content}

    history = get_memory(
        drawing_id=request_body.drawing_id
    )

    history = summarization(history,trigger=16)
    print(len(history))

    response = main_agent.invoke(
        {'messages':[sys_message]+history+[structured_user_input]}
    )

    print(response['structured_response'])

    send_memory(
        drawing_id=request_body.drawing_id,
        messages=history+[structured_user_input,response['structured_response']]
    )
    return response['structured_response']['content']


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

