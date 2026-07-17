from pathlib import Path

from models.httpRequestModels import IngestRequest
from models.httpResponseModels import IngestResponse
from utils.commonUtils import default_doc_type, read_utf8_file


def single_file_upload(payload: IngestRequest) -> IngestResponse:
    file_path = Path(payload.path).expanduser().resolve()
    document = read_utf8_file(file_path)
    doc_type = payload.doc_type.strip() if payload.doc_type else default_doc_type(file_path.name, payload.upload_type)
    document.metadata["doc_type"] = doc_type
    print(document)

    return IngestResponse(
        filename=file_path.name,
        docType=doc_type,
        filePath=str(file_path),
        fileSizeBytes=len(document.page_content.encode("utf-8")),
        status="read",
    )
