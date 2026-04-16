from pathlib import Path
from rag.file_loaders import iter_ingestible_files, extract_text
from rag.chunker import simple_chunk_text

def build_records_from_path(path: str, source: str) -> list[dict]:
    records = []
    for file_path in iter_ingestible_files(path):
        try:
            text = extract_text(Path(file_path))
        except Exception:
            continue
        for idx, chunk in enumerate(simple_chunk_text(text)):
            records.append({
                "text": chunk,
                "source": source,
                "path": str(file_path),
                "title": Path(file_path).name,
                "chunk_index": idx,
            })
    return records
