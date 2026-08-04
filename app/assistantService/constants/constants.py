from tenacity import wait_exponential

RETRIEVAL_K = 10 # surface up 10 chunks each retrieval call
FINAL_K = 10

AI_MODEL = "openai/gpt-4.1-nano"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
COLLECTION_TYPE_DOC = "documents"
FALLBACK_WAIT_TIME = wait_exponential(multiplier=1, min=10, max=240)
