from pydantic import BaseModel

class ChatModel(BaseModel):
    text: str

class TranslateModel(BaseModel):
    text: str