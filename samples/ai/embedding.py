import os

from openai import OpenAI

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


def open_ai_embedding(text: str) -> list[float]:
    assert OPEN_AI_API_KEY, "OPEN_AI_API_KEY environment variable not set"
    ai_client = OpenAI(api_key=OPEN_AI_API_KEY)
    embedding_vector = ai_client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return embedding_vector.data[0].embedding


if __name__ == '__main__':
    original_text = "Authentication tokens expire after 15 minutes."
    embedding_vector_list = open_ai_embedding(original_text)
    print(embedding_vector_list)
    print(f"Embedding length: {len(embedding_vector_list)}")
