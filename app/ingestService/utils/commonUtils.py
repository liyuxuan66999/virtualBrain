from pathlib import Path
import os
import re
from uuid import uuid4

from fastapi import HTTPException
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

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


def read_utf8_directory(
        folder_path: Path, 
        doc_type: str,
        user_id: str,
        kb_id: str,
        batch_id: str
    ) -> list[Document]:
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
        document.metadata["user_id"] = user_id
        document.metadata["kb_id"] = kb_id
        document.metadata["batch_id"] = batch_id
        document.metadata["document_id"] = f"doc_{uuid4().hex}"
        files_content.append(document)

    return files_content

def create_chunks(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 200,
) -> list[Document]:
    # chunk_size: tokens size in each chunk. 
	# Impacting MRR retrieval accuracy.
    print("creating chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = text_splitter.split_documents(documents)
    document_chunk_counts: dict[str, int] = {}
    for chunk in chunks:
        document_id = chunk.metadata.get("document_id")
        print("chunking document_id:", document_id)
        if not document_id:
            raise ValueError("chunk is missing document_id metadata")
        chunk_index = document_chunk_counts.get(document_id, 0)
        document_chunk_counts[document_id] = chunk_index + 1
        print("current chunk_index:",chunk_index)
        chunk.metadata["chunk_index"] = chunk_index
        print("current chunk_id:", f"{document_id}_chunk_{chunk_index}")
        chunk.metadata["chunk_id"] = f"{document_id}_chunk_{chunk_index}"

    return chunks

def create_embeddings(
        chunks,
        db_name,
        embeddings
    ):
    vectorstore = Chroma(
        collection_name="documents",
        persist_directory=db_name,
        embedding_function=embeddings,
    )
    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    vectorstore.add_documents(
        documents=chunks,
        ids=ids,
    )
    
    
    # optional: for testing or reporting
    collection = vectorstore._collection
    count = collection.count()
    sample_embedding = collection.get(
        limit=1, 
        include=["embeddings"]
    )["embeddings"][0]
    
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")
    #
    return vectorstore

