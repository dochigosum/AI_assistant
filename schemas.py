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

class NegativeGuardrail(BaseModel):
    """사용자의 질문에 욕이 포함되었는지에 대한 정보"""
    is_corrected : bool = Field(description="사용자의 질문에 욕이 사용되었는지")

class LearningGuardrail(BaseModel):
    """사용자의 질문이 적절한지에 대한 정보"""
    is_corrected : bool = Field(description="사용자의 질문이 적절한 질문인지 아닌지")

