from pathlib import Path

from fastapi import FastAPI, HTTPException

from models.httpRequestModels import IngestRequest
from models.httpResponseModels import IngestResponse
from utils.commonUtils import default_doc_type

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(payload: IngestRequest) -> IngestResponse:
    file_path = Path(payload.file_path).expanduser().resolve()

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="path is not a file")

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise HTTPException(status_code=400, detail="file must be utf-8 text") from error

    doc_type = payload.doc_type.strip() if payload.doc_type else default_doc_type(file_path.name)
    
    return IngestResponse(
        filename=file_path.name,
        docType=doc_type,
        filePath=str(file_path),
        fileSizeBytes=len(content.encode("utf-8")),
        status="read",
    )


def main():
    print("Hello from ingestservice!")


if __name__ == "__main__":
    main()
