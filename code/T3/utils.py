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
    
# Chat → text
def build_prompt(messages):
    """
    Convert chat messages to plain text prompt.
    Required for gpt-oss models.
    """
    text = ""
    for msg in messages:
        role = msg["role"].upper()
        text += f"{role}:\n{msg['content']}\n\n"
    text += "ASSISTANT:\n"
    return text