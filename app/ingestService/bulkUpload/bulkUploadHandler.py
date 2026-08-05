from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException
from langchain_openai import OpenAIEmbeddings

from models.httpRequestModels import IngestRequest
from models.httpResponseModels import BulkUploadResponse
from utils.commonUtils import default_doc_type, read_utf8_directory, create_chunks, create_embeddings
from utils.chunkingUtils import create_chunks_by_ai

async def bulk_upload(payload: IngestRequest) -> BulkUploadResponse:
    folder_path = Path(payload.path).expanduser().resolve()

    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="directory not found")

    if not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="path is not a directory")

    doc_type = payload.doc_type.strip() if payload.doc_type else default_doc_type(folder_path, payload.upload_type)
    # batch_id should be read from metadata DB later
    batch_id = f"batch_{uuid4().hex}"
    documents = read_utf8_directory(
        folder_path, 
        doc_type,
        payload.user_id,
        payload.kb_id,
        batch_id,
    )

    print("documents total count:",len(documents))
    # split documents into chunks
    # chunks = create_chunks(documents)
    chunks = create_chunks_by_ai(documents)
    print("created chunks:",chunks)

    # create vector DB 
    # ex1. /vector_db/tony/AMD
    # ex2. /vector_db/tom/password
    # each user will have multiple collections (kb_ids)
    # each collection (kb_id) can be created or selected by user
    db_name = str(
        Path(__file__).parent.parent
        / "vector_db"
        / payload.user_id
        / payload.kb_id
    )
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    print("db_name:", db_name)
    create_embeddings(
        chunks,
        db_name,
        embeddings
    )
    print("Ingestion complete")
    
    return BulkUploadResponse(
        directory=str(folder_path),
        docType=doc_type,
        fileCount=len(documents),
        status="read",
    )
