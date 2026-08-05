from datetime import datetime, UTC
from uuid import uuid4
from litellm import completion

from dotenv import load_dotenv
from fastapi import FastAPI

from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from chromadb import PersistentClient

from constants import constants
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages


from models import ChatRequest, ChatResponse
from utils.commonUtils import combined_question, fetch_context
from utils.queryUtils import make_rag_messages

app = FastAPI()
load_dotenv(override=True)

# mimic DB [conversation_id:[{msg_id:msg}]]
dummy_conversations: dict[str, list[dict[str, str]]] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/assistant/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    conversation_id = payload.conversation_id or str(uuid4())
    question = payload.message
    history = dummy_conversations.setdefault(conversation_id, [])
    dummy_user_message_id = str(uuid4())
    dummy_assistant_message_id = str(uuid4())
    
    # combined = combined_question(question, history)

    DB_DIR = Path("E:/Tony_learning/AI/projects/virtualBrain_v1/app/ingestService/vector_db")
    db_name = str(
        DB_DIR
        / payload.user_id
        / payload.kb_id
    )
    embeddings = OpenAIEmbeddings(model=constants.OPENAI_EMBEDDING_MODEL)
    chroma = PersistentClient(path=db_name)
    collection = chroma.get_or_create_collection(constants.COLLECTION_TYPE_DOC)

    chunks = fetch_context(
        db_name, 
        embeddings, 
        question, 
        history,
        collection
    )

    # next step complete rag AI call
    messages = make_rag_messages(question, history, chunks)
    print("rag message:",messages)
    response = completion(model=constants.AI_MODEL, messages=messages)

    history.append({"id": dummy_user_message_id, "role": "user", "content": question})
    history.append({"id": dummy_assistant_message_id, "role": "assistant", "content": response.choices[0].message.content})
            

    return ChatResponse(
        conversationId=conversation_id,
        userMessageId=dummy_user_message_id,
        assistantMessageId=dummy_assistant_message_id,
        answer=response.choices[0].message.content,
    )
