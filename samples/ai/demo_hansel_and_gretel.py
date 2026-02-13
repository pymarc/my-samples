
import numpy as np
from openai import OpenAI

from . import OPEN_AI_API_KEY

client = OpenAI(api_key=OPEN_AI_API_KEY)

story = [
"Beginning: Hansel and Gretel is a famous fairy tale about two children who get lost in the forest and must survive using cleverness and courage.",
"Beginning: Hansel and Gretel are poor siblings. Their parents (in many versions the stepmother) abandon them in the forest because the family has no food.",
"Beginning: The children try to find their way home.",
"Middle of the story: They discover a house made of sweets and gingerbread.",
"Middle of the story: An old woman (a witch) lives there and pretends to be kind.",
"Middle of the story: The witch plans to eat the children.",
"The end: Gretel tricks the witch and pushes her into the oven.",
"The end: The children escape with treasure and safely return home.",
"Main themes (what the fairy tale teaches): be careful with strangers, intelligence can save you in danger, courage and cooperation help overcome problems, greed and cruelty are punished"
]

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


if __name__ == '__main__':
    # Knowledge part
    story_resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=story
    )
    story_embeddings = [d.embedding for d in story_resp.data]

    # Question part
    question = "What is Hansel and Gretel?"
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    # Top-k
    k = 5
    threshold = 0.6
    scored = [(line, cosine(q_emb, l_emb)) for line, l_emb in zip(story, story_embeddings)]
    scored.sort(key=lambda x: x[1], reverse=True)
    selected = [(l, sc) for l, sc in scored[:k] if sc >= threshold]

    if not selected:
        selected = scored[:2]

    context = '\n'.join(f"- {line}" for line, _ in selected)

    prompt = f"""You are a helpful assistant. Answer ONLY using the provided context.
    If the answer is not in the context, say you don't know.
    
    Context:
    {context}
    
    Question:
    {question}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    print("\n--- Retrieval (top) ---")
    for d, s in selected:
        print(f"{s:.3f} -> {d}")

    print("\n--- Answer (top) ---")
    print(response.output_text)
