
from . import OPEN_AI_API_KEY

import numpy as np
from openai import OpenAI

client = OpenAI(api_key=OPEN_AI_API_KEY)


if __name__ == '__main__':
    docs = [
        "Authentication tokens expire after 15 minutes.",
        "Use /auth/refresh to renew tokens.",
        "Invalid tokens return HTTP 401.",
        "Passwords must contain at least 8 characters.",
        "The database runs on PostgreSQL."
    ]

    doc_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=docs
    )

    doc_embeddings = [doc_data.embedding for doc_data in doc_response.data]

    query = "How do I refresh my token?"

    query_embedding_ = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding


    # check cosine similarity of embedding vectors
    def cosine_similarity(query_embedding, knowledge_embedding):
        query_embedding = np.array(query_embedding)
        knowledge_embedding = np.array(knowledge_embedding)
        return np.dot(
            query_embedding, knowledge_embedding
        ) / (np.linalg.norm(query_embedding) * np.linalg.norm(knowledge_embedding))

    scores = [cosine_similarity(query_embedding_, emb) for emb in doc_embeddings]

    # top-k
    k = 3
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    print("Question: ", query)
    print(f"Top {k} results:")
    for doc, score in ranked[:k]:
        print(f"{doc}: {score}")
