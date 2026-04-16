from pathlib import Path
from pypdf import PdfReader
import json
import os

TEXT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".py", ".java", ".js", ".ts", ".tsx", ".jsx", ".go",
    ".rs", ".c", ".cpp", ".h", ".hpp", ".cs", ".sql", ".yaml", ".yml", ".json",
    ".xml", ".html", ".css", ".sh"
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", "dist", "build", ".venv", "venv"}

def iter_ingestible_files(input_path: str):
    root = Path(input_path)
    if root.is_file():
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() in TEXT_EXTENSIONS or path.suffix.lower() == ".pdf":
                yield path

def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        return json.dumps(data, indent=2)
    return path.read_text(encoding="utf-8", errors="ignore")
