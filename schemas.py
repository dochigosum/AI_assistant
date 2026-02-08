json_schema = {
    "title": "AIResponse",
    "description": "사용자의 질문에 대한 AI의 답변 구조",
    "type": "object",
    "properties": {
        "role": {
            "type": "string",
            "description": "응답자의 역할 (예: ai)",
            "const": "ai"
        },
        "content": {
            "type": "string",
            "description": "사용자의 질문에 대한 구체적인 답변 내용"
        }
    },
    "required": ["role", "content"]
}

from pydantic import BaseModel, Field

class CustomGuardrail(BaseModel):
    """학습에 관련된 정보인지 아닌지 정보"""
    is_corrected : bool = Field(description="인풋이 학습에 관련된 내용인지 아닌지")