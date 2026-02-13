
import numpy as np
from openai import OpenAI

from . import OPEN_AI_API_KEY

client = OpenAI(api_key=OPEN_AI_API_KEY)


if __name__ == '__main__':
    docs = [
        "Authentication tokens expire after 15 minutes.",
        "Use /auth/refresh to renew tokens.",
        "Invalid tokens return HTTP 401.",
        "Passwords must contain at least 8 characters.",
        "The database runs on PostgreSQL."
    ]

    # 1) Embed docs (batch)
    doc_resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=docs
    )
    doc_embeddings = [d.embedding for d in doc_resp.data]

    # 2) Embed query
    question = "How do I refresh my token?"
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding


    def cosine(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    # 3) Top-k + threshold
    k = 5
    threshold = 0.55

    scored = [(doc, cosine(q_emb, emb)) for doc, emb in zip(docs, doc_embeddings)]
    scored.sort(key=lambda x: x[1], reverse=True)

    selected = [(d, s) for d, s in scored[:k] if s >= threshold]

    if not selected:
        selected = scored[:2]

    context = "\n".join([f"- {d}" for d, _ in selected])

    # 4) Ask LLM with context
    prompt = f"""You are a helpful assistant. Answer ONLY using the provided context.
    If the answer is not in the context, say you don't know.

    Context:
    {context}

    Question: {question}
    """

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    print("\n--- Retrieval (top) ---")
    for d, s in selected:
        print(f"{s:.3f} -> {d}")

    print("\n--- Answer ---")
    print(resp.output_text)

