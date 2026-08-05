from pydantic import BaseModel, Field
from uuid import uuid4

class Result(BaseModel):
    page_content: str
    metadata: dict

class Chunk(BaseModel):
    headline: str = Field(
        description="A brief heading for this chunk, typically a few words, that is most likely to be surfaced in a query",
    )
    summary: str = Field(
        description="A few sentences summarizing the content of this chunk to answer common questions"
    )
    original_text: str = Field(
        description="The original text of this chunk from the provided document, exactly as is, not changed in any way"
    )

    def as_result(self, document):
        print("doc meta data:",document)
        document_id = document.metadata["document_id"]
        chunk_uuid = uuid4()
        metadata = {
            "source": document.metadata["source"], 
            "type": document.metadata["doc_type"],
            "chunk_id": f"{document_id}_chunk_{chunk_uuid}"
        }
        return Result(
            page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata,
        )

class Chunks(BaseModel):
    chunks: list[Chunk]