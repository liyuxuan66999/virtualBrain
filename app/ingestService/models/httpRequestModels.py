from pydantic import BaseModel, ConfigDict, Field


class IngestRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    file_path: str = Field(alias="filePath", min_length=1)
    doc_type: str | None = Field(default=None, alias="docType", min_length=1)

