import yaml
import re
from app.config_loader import load_rules

def _load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

branches_cfg = _load_yaml("config/branches.yaml")
rules_cfg = _load_yaml("config/rules.yaml")

def detect_branch(text):
    text = text.lower()

    for branch, data in branches_cfg["branches"].items():
        for kw in data["keywords"]:
            if kw.lower() in text:
                return branch

    return None

def detect_doc_type(text: str):
    rules = load_rules()
    text = text.upper()

    for doc_type, cfg in rules["document_types"].items():
        patterns = cfg.get("filename_patterns", [])
        for pattern in patterns:
            if re.search(pattern.upper(), text):
                return doc_type

    return None
