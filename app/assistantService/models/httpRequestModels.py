from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId", min_length=1)
    kb_id: str = Field(alias="kbId", min_length=1)
    conversation_id: str | None = Field(default=None, alias="conversationId")
    message: str = Field(min_length=1)
