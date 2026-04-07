
import json
from pathlib import Path
from markdown_it import MarkdownIt
from argparse import ArgumentParser
from openai import OpenAI

from samples.time_machine_helpdesk import OPEN_AI_API_KEY


def chunking(markdown_content: str):
    markdown_it = MarkdownIt()
    markdown_data = markdown_it.parse(markdown_content)

    is_header_name = False
    current_header = ''
    text_lines = []
    for token in markdown_data:
        if token.type == 'heading_open':
            is_header_name = True
        elif token.type == 'inline' and isinstance(token.content, str) and token.content:
            if is_header_name:
                current_header = token.content
                is_header_name = False
            else:
                text_lines.append(f'{current_header}: {token.content}')

    return text_lines


def embedding(docs_lines: list[str]) -> list[tuple[str, list[float]]]:
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    docs_embedding_obj = client.embeddings.create(
        model="text-embedding-3-small",
        input=docs_lines
    )
    docs_embeddings = [d.embedding for d in docs_embedding_obj.data]
    return list(zip(docs_lines, docs_embeddings))


def save_embedding():
    pass


def main(documentation_file_path: Path, output_jsonl: Path):
    with documentation_file_path.open('r') as file:
        markdown_content = file.read()
    docs_lines = chunking(markdown_content)
    docs_line_and_embedding: list[tuple[str, list[float]]]= embedding(docs_lines)
    jsonl_list = [
        json.dumps({"line": line, "embedding": embedding_value})
        for line, embedding_value in docs_line_and_embedding
    ]
    jsonl_str = '\n'.join(jsonl_list)
    with output_jsonl.open('w') as output_file:
        output_file.write(jsonl_str)


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument(
        '--doc-file', '-d',
        type=str, required=True, help='Path to the document MD file.'
    )
    args_parser.add_argument(
        '--output-jsonl', '-o',
        type=str, required=True, help='Path to the output JSONL file with embeddings.'
    )
    args = args_parser.parse_args()
    main(Path(args.doc_file), Path(args.output_jsonl))
