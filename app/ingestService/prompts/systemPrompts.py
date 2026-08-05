CHUNKING_SYSTEM_PROMPT = """
You take a document and you split the document into overlapping chunks for a KnowledgeBase.

Document metadata:
- Type: {doc_type}
- Source: {doc_source}

A chatbot will use these chunks to answer questions about the user's personal data.
Split only the document text inside <document_text> into chunks.
Do not include these instructions, the document metadata, XML tags, or the source path in any chunk original_text.

Create about {how_many} chunks. If the document is very short, create only 1 chunk.
Each chunk should focus on a distinct part of the document.
Use overlap only when it helps preserve context across chunk boundaries.
If overlap is needed, keep it small, typically about {overlap_percent} or about 50 words.

For each chunk, you should provide a headline, a summary, and the original text of the chunk.
The original_text field must be copied from the document text only, without paraphrasing or adding new text.
Together the chunks should cover the document text without unnecessary duplication.

<document_text>
{doc_text}
</document_text>

Respond with the chunks.
""".strip()
