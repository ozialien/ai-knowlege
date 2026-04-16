from __future__ import annotations
import os
import json
from pathlib import Path
from pypdf import PdfReader

TEXT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".py", ".java", ".js", ".ts", ".tsx", ".jsx", ".go",
    ".rs", ".c", ".cpp", ".h", ".hpp", ".cs", ".sql", ".yaml", ".yml", ".json",
    ".xml", ".html", ".css", ".sh", ".bash", ".zsh"
}

SKIP_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", "node_modules", "dist", "build",
    ".venv", "venv", "target", ".mypy_cache", ".pytest_cache"
}

MAX_FILE_BYTES = 1_500_000

def should_skip_path(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def load_json_file(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    return json.dumps(data, indent=2)

def load_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return load_pdf_file(path)
    if path.suffix.lower() == ".json":
        return load_json_file(path)
    return load_text_file(path)

def iter_ingestible_files(input_path: str) -> list[Path]:
    root = Path(input_path)
    if not root.exists():
        raise FileNotFoundError(f"Path not found: {input_path}")
    if root.is_file():
        return [root]
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if should_skip_path(path):
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS and path.suffix.lower() != ".pdf":
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            files.append(path)
    return files
