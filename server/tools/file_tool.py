import os
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

def list_workspace_files(sub_dir=""):
    target_path = WORKSPACE_ROOT / sub_dir
    # Safety boundary check
    if not str(target_path.resolve()).startswith(str(WORKSPACE_ROOT.resolve())):
        return "Access denied: outside workspace bounds."
    try:
        items = os.listdir(target_path)
        return [
            {"name": item, "type": "directory" if (target_path / item).is_dir() else "file"}
            for item in items if not item.startswith(".")
        ]
    except Exception as e:
        return f"FileSystem error listing files: {e}"

def read_workspace_file(file_path):
    target_file = WORKSPACE_ROOT / file_path
    if not str(target_file.resolve()).startswith(str(WORKSPACE_ROOT.resolve())):
        return "Access denied: outside workspace bounds."
    try:
        if not target_file.is_file():
            return "File not found."
        with open(target_file, "r", encoding="utf-8") as f:
            return f.read()[:2000] # return top excerpt
    except Exception as e:
        return f"FileSystem error reading file: {e}"
