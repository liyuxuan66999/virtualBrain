from tenacity import wait_exponential

WORKERS = 3
FALLBACK_WAIT_TIME = wait_exponential(multiplier=1, min=10, max=240)
RETRY_LIMIT = 2
AI_MODEL = "openai/gpt-4.1-nano"
AVERAGE_CHUNK_SIZE = 100
DEFAULT_CHUNK_OVERLAP = "25%"