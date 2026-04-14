from rag.chunker import simple_chunk_text

def test_chunker_returns_chunks():
    text = "a" * 2500
    chunks = simple_chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 5
