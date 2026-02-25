import os
import re
import json
import pandas as pd

# Utility to ensure file existence with optional columns
def ensure_file(file_path, columns=None):
    try:
        if not os.path.exists(file_path):
            if columns is None:
                columns = []
            pd.DataFrame(columns=columns).to_csv(file_path, index=False)
        return file_path
    except Exception:
        print(f"Error ensuring file {file_path}.")
        return None

# JSON extractor
def extract_json(text, pattern=r"\{[\s\S]*?\}"):
    match = re.search(pattern, text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None

def load_existing_ids(path, column='id'):
    try:
        existing_ids = set(pd.read_csv(path)["id"].astype(str))
    except Exception:
        existing_ids = set()
    print(f"Already processed {len(existing_ids)} videos.")

    return existing_ids

def extract_label(text):
    match = re.search(r'\b(True|False)\b', text.strip())
    if match:
        return match.group(1)
    return "INVALID"