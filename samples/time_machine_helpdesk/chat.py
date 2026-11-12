"""A simple AI chat for getting information about the time machine named ChronoShift."""
import sys
import json
import time
import logging
import numpy as np
from openai import OpenAI
from pathlib import Path
from argparse import ArgumentParser

from samples.time_machine_helpdesk import OPEN_AI_API_KEY

client = OpenAI(api_key=OPEN_AI_API_KEY)


def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve_docs_embedding(docs_embedding_jsonl_path: Path) -> list[tuple[str, list[float]]]:
    output = []
    with docs_embedding_jsonl_path.open('r') as f:
        for line in f:
            try:
                jsonl_data = json.loads(line)
                output.append(
                    (jsonl_data['line'], jsonl_data['embedding'])
                )
            except json.JSONDecodeError:
                logging.warning(f"Failed to parse JSON line: {line}")
                continue
    return output


def answer(question: str, docs_embedding: list[tuple[str, list[float]]]) -> str:
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    # Top-k
    k = 4
    threshold = 0.6
    scored = [(line, cosine(q_emb, l_emb)) for line, l_emb in docs_embedding]
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

    logging.info(f"Selected lines from the documentation: {selected}")

    return response.output_text


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument(
        '--docs-embedding-path', '-d',
        type=Path, required=True, help='Path to the JSONL file containing documentation embeddings.'
    )
    args = args_parser.parse_args()
    docs_embedding_ = retrieve_docs_embedding(args.docs_embedding_path)

    while True:
        # question_ = "What is ChronoShift X1?"
        try:
            question_ = input("Question: ")
            t0 = time.perf_counter()
        except KeyboardInterrupt:
            sys.exit(0)
        print('.......')
        answer_ = answer(question_, docs_embedding_)
        waited = time.perf_counter() - t0
        print(f"Answer [waited {waited:.3f} s]: {answer_}")
