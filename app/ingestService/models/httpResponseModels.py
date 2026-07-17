from pydantic import BaseModel, ConfigDict, Field


class IngestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    filename: str
    doc_type: str = Field(alias="docType")
    file_path: str = Field(alias="filePath")
    file_size_bytes: int = Field(alias="fileSizeBytes")
    status: str


# class BulkUploadFileResponse(BaseModel):
#     model_config = ConfigDict(populate_by_name=True)

#     filename: str
#     doc_type: str = Field(alias="docType")
#     file_path: str = Field(alias="filePath")
#     file_size_bytes: int = Field(alias="fileSizeBytes")


class BulkUploadResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    directory: str
    doc_type: str = Field(alias="docType")
    file_count: int = Field(alias="fileCount")
    status: str
