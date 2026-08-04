from tenacity import retry, wait_exponential
from litellm import completion
from constants import constants
from models import rankingModels



# fallback mechanism retry the same function in 
# exponential wait time
@retry(wait= constants.FALLBACK_WAIT_TIME)
def rewrite_query(question, history):
    """Rewrite the user's question to be a more specific 
    question that is more likely to surface relevant content 
    in the Knowledge Base."""
    message = f"""
    You are in a conversation with a user, answering questions 
    about the user's past peronal experience could be personal or 
    work related etc.
    You are about to look up information in a Knowledge 
    Base to answer the user's question.

    This is the history of your conversation so far with the user:
    {history}

    And this is the user's current question:
    {question}

    Respond only with a short, refined question that you 
    will use to search the Knowledge Base.
    It should be a VERY short specific question most 
    likely to surface content. Focus on the question details.
    IMPORTANT: Respond ONLY with the precise knowledgebase 
    query, nothing else.
    """
    response = completion(model=constants.AI_MODEL, messages=[{"role": "system", "content": message}])
    return response.choices[0].message.content

@retry(wait=constants.FALLBACK_WAIT_TIME)
def rerank(question, chunks):
    system_prompt = """
        You are a document re-ranker.
        You are provided with a question and a list of relevant chunks of text from a query of a knowledge base.
        The chunks are provided in the order they were retrieved; this should be approximately ordered by relevance, but you may be able to improve on that.
        You must rank order the provided chunks by relevance to the question, with the most relevant chunk first.
        Reply only with the list of ranked chunk ids, nothing else. Include all the chunk ids you are provided with, reranked.
    """
    user_prompt = f"The user has asked the following question:\n\n{question}\n\nOrder all the chunks of text by relevance to the question, from most relevant to least relevant. Include all the chunk ids you are provided with, reranked.\n\n"
    user_prompt += "Here are the chunks:\n\n"
    for index, chunk in enumerate(chunks):
        user_prompt += f"# CHUNK ID: {index + 1}:\n\n{chunk.page_content}\n\n"
    user_prompt += "Reply only with the list of ranked chunk ids, nothing else."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = completion(model=constants.AI_MODEL, messages=messages, response_format=rankingModels.RankOrder)
    reply = response.choices[0].message.content
    order = rankingModels.RankOrder.model_validate_json(reply).order
    return [chunks[i - 1] for i in order]