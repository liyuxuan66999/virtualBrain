from constants import constants
from models import chunkingModels


def fetch_context_unranked(question, embeddings, collection):
    # query = openai.embeddings.create(model=constants.OPENAI_EMBEDDING_MODEL, input=[question]).data[0].embedding
    query = embeddings.embed_query(question)
    results = collection.query(
        query_embeddings=[query],
        n_results=constants.RETRIEVAL_K,
    )
    chunks = []
    for result in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(chunkingModels.Result(page_content=result[0], metadata=result[1]))
    return chunks


def merge_chunks(chunks, reranked):
    merged = chunks[:]
    existing = [chunk.page_content for chunk in chunks]
    for chunk in reranked:
        if chunk.page_content not in existing:
            merged.append(chunk)
    return merged
