from langchain_core.documents import Document
from constants import constants
from utils.chunkingUtils import fetch_context_unranked, merge_chunks
from utils.queryUtils import rewrite_query, rerank



def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question

def fetch_context(
        db_name: str, 
        embeddings, 
        question: str, 
        history,
        collection
    ) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    # vectorstore = Chroma(
    #     collection_name=constants.COLLECTION_TYPE_DOC,
    #     persist_directory=db_name,
    #     embedding_function=embeddings,
    # )
    # retriever = vectorstore.as_retriever(search_kwargs={"k": constants.RETRIEVAL_K})
    ai_rewritten_question = rewrite_query(question, history)
    chunks_by_originQ = fetch_context_unranked(question, embeddings, collection)
    print("collection count:", collection.count())
    # print("chunks fetched by originQ:", chunks_by_originQ.count())
    chunks_by_ai_rewrittenQ = fetch_context_unranked(ai_rewritten_question, embeddings, collection)
    # print("chunks fetched by AI regenerated Q:", chunks_by_ai_rewrittenQ)
    chunks = merge_chunks(chunks_by_originQ, chunks_by_ai_rewrittenQ)
    reranked = rerank(question, chunks)
    print("reranked:",reranked)
    return reranked[:constants.FINAL_K]
