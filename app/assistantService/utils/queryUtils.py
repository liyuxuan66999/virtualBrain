from tenacity import retry, wait_exponential
from litellm import completion
from constants import constants
from models import rankingModels
from prompts import systemPrompts



# fallback mechanism retry the same function in 
# exponential wait time
@retry(wait= constants.FALLBACK_WAIT_TIME)
def rewrite_query(question, history):
    """Rewrite the user's question to be a more specific 
    question that is more likely to surface relevant content 
    in the Knowledge Base."""
    message = systemPrompts.REWRITE_QUERY_SYSTEM_PROMPT.format(
        history=history,
        question=question,
    )
    response = completion(model=constants.AI_MODEL, messages=[{"role": "system", "content": message}])
    return response.choices[0].message.content

@retry(wait=constants.FALLBACK_WAIT_TIME)
def rerank(question, chunks):
    user_prompt = f"The user has asked the following question:\n\n{question}\n\nOrder all the chunks of text by relevance to the question, from most relevant to least relevant. Include all the chunk ids you are provided with, reranked.\n\n"
    user_prompt += "Here are the chunks:\n\n"
    for index, chunk in enumerate(chunks):
        user_prompt += f"# CHUNK ID: {index + 1}:\n\n{chunk.page_content}\n\n"
    user_prompt += "Reply only with the list of ranked chunk ids, nothing else."
    messages = [
        {"role": "system", "content": systemPrompts.RERANKER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    response = completion(model=constants.AI_MODEL, messages=messages, response_format=rankingModels.RankOrder)
    reply = response.choices[0].message.content
    order = rankingModels.RankOrder.model_validate_json(reply).order
    return [chunks[i - 1] for i in order]

def make_rag_messages(question, history, chunks):
    context = "\n\n".join(
        f"Extract from {chunk.metadata['source']}:\n{chunk.page_content}" for chunk in chunks
    )
    system_prompt = systemPrompts.ASSISSTANT_SYSTEM_PROMPT.format(context=context)
    processedHistory = [
        {"role": message["role"], "content": message["content"]}
        for message in history
    ]
    return (
        [{"role": "system", "content": system_prompt}]
        + processedHistory
        + [{"role": "user", "content": question}]
    )
