from pathlib import Path
from fastapi import HTTPException

from models.httpRequestModels import IngestRequest
from models.httpResponseModels import BulkUploadResponse
from utils.commonUtils import default_doc_type, read_utf8_directory, create_chunks


def bulk_upload(payload: IngestRequest) -> BulkUploadResponse:
    folder_path = Path(payload.path).expanduser().resolve()

    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="directory not found")

    if not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="path is not a directory")

    doc_type = payload.doc_type.strip() if payload.doc_type else default_doc_type(folder_path, payload.upload_type)
    documents = read_utf8_directory(folder_path, doc_type)

    print(documents)
    # split documents into chunks
    chunks = create_chunks(documents)
    print("chunks:", chunks)
    
    return BulkUploadResponse(
        directory=str(folder_path),
        docType=doc_type,
        fileCount=len(documents),
        status="read",
    )
