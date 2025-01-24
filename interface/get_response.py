from RAG.utils import cos_similarity
from pinecone import Pinecone
import os
import pandas as pd
    
    
# use cached embeddings in parquet file
def retrieve_context(query, cards, embedding, model, top_k):
    """
    Retrieves the top-k most relevant contexts from a corpus based on a given query using cosine similarity.

    :param query: The query string for which context is to be retrieved.
    :param embedding: A pandas DataFrame containing the precomputed embeddings of the corpus with columns 'embedding' and 'text'.
    :param model: The model used to encode the query into an embedding.
    :param top_k: The number of top contexts to retrieve based on similarity.

    :return: A string concatenating the top-k contexts, each preceded by a '#' and separated by new lines.
    """

    pc = Pinecone(api_key=os.getenv("PINECONE"))
    index = pc.Index("astrology-bot")

    # get embedding
    corpus_embedding = embedding["embedding"].tolist()
    query_embedding = model.encode([query], show_progress_bar=False)
    
    
    # #compute sim score
    # sim_score = cos_similarity(query_embedding, corpus_embedding)
    
    # retrieve context
    # scores, corpus_id = torch.topk(sim_score, top_k, dim=1)
    matches = index.query(vector=query_embedding.tolist(),
                            top_k=top_k,
                            include_values=True,
                            include_metadata=True,
                            filter={"topic": {"$in": cards}}
                        )

    context = ""
    for i,match in enumerate(matches['matches']):
        context += f"#{str(i)} {match['metadata']['text']} \n"
        

    # # merge context into prompt
    # context = " \n ".join([f"#{str(i)}" for i in retrieve_context])
    
    return context


def ask_question(question, context, inference_model, cards):
    """
    Generates an answer to a given question using a few-shot learning approach and provided context.

    :param question: The question to be answered.
    :param few_shots: Examples provided to guide the model in the format of few-shot learning.
    :param context: The context or background information relevant to the question.
    :param inference_model: The model used to infer or predict the answer based on the query.

    :return: The predicted answer as a string, expected to be one word among [A, B, C, D].
    """
    
    query = f"""You are an AI Clairvoyant. The retrieved context may help answer the question.

    Context: {context}

    Question: {question}

    Tarot Cards: {cards}

    Response to the Question:
    """
    
    answer = inference_model.predict(query)
    
    return answer