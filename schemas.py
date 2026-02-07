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