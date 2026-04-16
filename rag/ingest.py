from pathlib import Path
from rag.chunker import simple_chunk_text
from rag.file_loaders import iter_ingestible_files, extract_text_from_file

def prepare_texts(texts: list[str]) -> list[str]:
    out = []
    for text in texts:
        out.extend(simple_chunk_text(text))
    return out

def prepare_path(path: str) -> list[dict]:
    records = []
    for file_path in iter_ingestible_files(path):
        text = extract_text_from_file(file_path)
        if not text.strip():
            continue
        chunks = simple_chunk_text(text)
        for idx, chunk in enumerate(chunks):
            records.append({
                "text": chunk,
                "path": str(file_path),
                "chunk_index": idx,
                "title": Path(file_path).name,
            })
    return records
