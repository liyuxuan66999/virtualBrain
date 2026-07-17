from pathlib import Path
import os
import re

from fastapi import HTTPException
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.httpRequestModels import UploadType


def default_doc_type(path: str | Path, upload_type: UploadType) -> str:
    if upload_type == UploadType.bulk_upload:
        return os.path.basename(Path(path)) or "document"

    file_stem = Path(path).stem.lower()
    doc_type = re.sub(r"[^a-z0-9]+", "_", file_stem).strip("_")
    return doc_type or "document"


def read_utf8_file(file_path: Path) -> Document:
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="path is not a file")

    try:
        documents = TextLoader(str(file_path), encoding="utf-8").load()
    except (RuntimeError, UnicodeDecodeError) as error:
        raise HTTPException(status_code=400, detail="file must be utf-8 text") from error

    if not documents:
        raise HTTPException(status_code=400, detail="file could not be loaded")

    return documents[0]


def read_utf8_directory(folder_path: Path, doc_type: str) -> list[Document]:
    loader = DirectoryLoader(
        str(folder_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    files_content = []
    for document in documents:
        source_path = Path(document.metadata["source"]).resolve()
        print("uploading file:", source_path)
        document.metadata["doc_type"] = doc_type
        files_content.append(document)

    return files_content

def create_chunks(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 200,
) -> list[Document]:
    # chunk_size: tokens size in each chunk. 
	# Impacting MRR retrieval accuracy.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
