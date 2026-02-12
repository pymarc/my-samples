import tiktoken
from openai import OpenAI

from . import OPEN_AI_API_KEY


def open_ai_embedding(text: str) -> list[float]:
    assert OPEN_AI_API_KEY, "OPEN_AI_API_KEY environment variable not set"
    ai_client = OpenAI(api_key=OPEN_AI_API_KEY)
    embedding_vector = ai_client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    print(embedding_vector)
    return embedding_vector.data[0].embedding


def get_tokens(text: str) -> list[int]:
    encoder = tiktoken.encoding_for_model('text-embedding-3-small')
    result = encoder.encode(text)
    return result
