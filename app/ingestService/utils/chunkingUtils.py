from tenacity import retry, stop_after_attempt
from litellm import completion
from tqdm import tqdm
from multiprocessing import Pool
from langchain_core.documents import Document

from constants import constants
from utils.queryUtils import make_messages
from models import chunkModels

@retry(wait=constants.FALLBACK_WAIT_TIME, stop=stop_after_attempt(constants.RETRY_LIMIT))
def process_document(document):
    messages = make_messages(document)
    print("chunking with AI")
    response = completion(model=constants.AI_MODEL, messages=messages, response_format=chunkModels.Chunks)
    reply = response.choices[0].message.content
    doc_as_chunks = chunkModels.Chunks.model_validate_json(reply).chunks
    return [chunk.as_result(document) for chunk in doc_as_chunks]

def create_chunks_by_ai(
    documents: list[Document],
) -> list[Document]:
    """
    Create chunks using a number of workers in parallel.
    If you get a rate limit error, set the WORKERS to 1.
    """
    chunks = []
    with Pool(processes=constants.WORKERS) as pool:
            for result in tqdm(pool.imap_unordered(process_document, documents), total=len(documents)):
                chunks.extend(result)
    return chunks
