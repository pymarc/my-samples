
import tiktoken
from .embedding import open_ai_embedding, get_tokens


if __name__ == '__main__':
    original_text = "Authentication tokens expire after 15 minutes."
    tokens = get_tokens(original_text)
    print(f"There will be {len(tokens)} tokens.")
    print("How the text was cut to tokens...")
    encoder_ = tiktoken.encoding_for_model('text-embedding-3-small')
    fragments = [encoder_.decode([t]) for t in tokens]
    print(fragments)

    embedding_vector_list = open_ai_embedding(original_text)
    print(embedding_vector_list)
    print(f"Embedding length: {len(embedding_vector_list)}")
