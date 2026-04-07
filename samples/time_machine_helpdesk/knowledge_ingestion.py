
from pathlib import Path
from markdown_it import MarkdownIt
from argparse import ArgumentParser


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

    pass


def embedding():
    pass


def save_embedding():
    pass


def main(documentation_file_path: Path):
    with documentation_file_path.open('r') as file:
        markdown_content = file.read()
    chunking(markdown_content)


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument(
        '--doc-file', '-d',
        type=str, required=True, help='Path to the document file'
    )
    args = args_parser.parse_args()
    main(Path(args.doc_file))
