from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from fileUpload.singleFileUploadHandler import single_file_upload
from bulkUpload.bulkUploadHandler import bulk_upload
from models.httpRequestModels import IngestRequest, UploadType
from models.httpResponseModels import BulkUploadResponse, IngestResponse

app = FastAPI()
load_dotenv(override=True)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse | BulkUploadResponse)
def ingest(payload: IngestRequest) -> IngestResponse | BulkUploadResponse:
    if payload.upload_type == UploadType.file_upload:
        return single_file_upload(payload)
    
    if payload.upload_type == UploadType.bulk_upload:
        return bulk_upload(payload)

    raise HTTPException(status_code=501, detail="bulk upload is not implemented")
