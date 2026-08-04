from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    id: str
    role: str
    content: str
    created_at: str = Field(alias="createdAt")


class ChatResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    conversation_id: str = Field(alias="conversationId")
    user_message_id: str = Field(alias="userMessageId")
    assistant_message_id: str = Field(alias="assistantMessageId")
    answer: str
