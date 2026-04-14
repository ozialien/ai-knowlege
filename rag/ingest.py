from rag.chunker import simple_chunk_text

def prepare_texts(texts: list[str]) -> list[str]:
    output = []
    for text in texts:
        output.extend(simple_chunk_text(text))
    return output
