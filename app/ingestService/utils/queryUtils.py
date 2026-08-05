from constants import constants
from prompts import systemPrompts

def make_prompt(document):
    how_many = (len(document.page_content) // constants.AVERAGE_CHUNK_SIZE) + 1
    return systemPrompts.CHUNKING_SYSTEM_PROMPT.format(
        doc_type = document.metadata["doc_type"],
        doc_source = document.metadata["source"],
        how_many = how_many,
        overlap_percent = constants.DEFAULT_CHUNK_OVERLAP,
        doc_text = document.page_content
    )



def make_messages(document):
    print("generating chunking messages")
    return [
        {"role": "user", "content": make_prompt(document)},
    ]