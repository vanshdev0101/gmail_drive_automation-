from pathlib import Path

ROOT = Path("Sarvana")

BRANCHES = [
    "Madurai",
    "Selvarathnam",
    "Tirunelveli",
    "Pallavaram"
]

DOC_TYPES = ["GRN", "po", "DB", "LR"]


def ensure_structure():
    for branch in BRANCHES:
        for doc in DOC_TYPES:
            path = ROOT / branch / doc
            path.mkdir(parents=True, exist_ok=True)

            keep = path / ".keep"
            if not any(path.iterdir()):
                keep.touch(exist_ok=True)

def get_target_folder(branch, doc_type):
    path = ROOT / branch / doc_type
    path.mkdir(parents=True, exist_ok=True)

    keep = path / ".keep"
    if keep.exists():
        keep.unlink()

    return path
