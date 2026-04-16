from apps.api.config import settings

def simple_chunk_text(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunk_size = settings.max_chunk_size
    overlap = settings.chunk_overlap
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks
