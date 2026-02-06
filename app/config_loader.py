from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_rules():
    rules_path = CONFIG_DIR / "rules.yaml"
    branches_path = CONFIG_DIR / "branches.yaml"

    if not rules_path.exists():
        raise FileNotFoundError(f"Missing rules.yaml at {rules_path}")

    if not branches_path.exists():
        raise FileNotFoundError(f"Missing branches.yaml at {branches_path}")

    with open(rules_path, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    with open(branches_path, "r", encoding="utf-8") as f:
        branches = yaml.safe_load(f)

    return {
        "document_types": rules.get("document_types", {}),
        "branches": branches.get("branches", {})
    }
