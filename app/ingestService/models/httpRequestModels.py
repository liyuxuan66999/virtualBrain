from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class UploadType(str, Enum):
    bulk_upload = "bulkUpload"
    file_upload = "fileUpload"


class IngestRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    path: str = Field(alias="directory", min_length=1)
    upload_type: UploadType = Field(default=UploadType.file_upload, alias="uploadType")
    doc_type: str | None = Field(default=None, alias="docType", min_length=1)
    user_id: str = Field(alias="userId", min_length=1)
    kb_id: str = Field(alias="kbId", min_length=1)