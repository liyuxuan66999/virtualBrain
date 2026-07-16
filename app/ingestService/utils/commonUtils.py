from pathlib import Path
import re


def default_doc_type(filename: str) -> str:
    file_stem = Path(filename).stem.lower()
    doc_type = re.sub(r"[^a-z0-9]+", "_", file_stem).strip("_")
    return doc_type or "document"
