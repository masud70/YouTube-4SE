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

def get_instruction():
    instruction = [
        {
            "role": "SYSTEM",
            "content": """You are a strict binary classifier for Software Engineering educational content.

                    Definition of Software Engineering educational content:
                    Software Engineering YouTube videos that contribute to Software Engineering (SE) education worldwide, grounded in the knowledge areas defined by the SWEBOK Guide V4.0a. Software Engineering is defined as the systematic, disciplined, and measurable approach to the specification, design, construction, testing, deployment, operation, maintenance, management, and evolution of software systems. The scope includes content aligned with SWEBOK knowledge areas such as Software Requirements, Architecture, Design, Construction, Testing, Maintenance, Configuration Management, Engineering Operations (including DevOps and release engineering), Software Engineering Management, Process, Models and Methods, Software Quality, Software Security, Professional Practice, and Software Engineering Economics. It also includes research-oriented topics—such as empirical software engineering, software metrics, AI for software engineering, secure development life cycles, and process improvement—when they directly relate to improving software systems or engineering practices. Foundational topics from Computing, Mathematical, and Engineering Foundations are included only when presented in support of software engineering activities (e.g., algorithms for software performance, AI in SE, networking for distributed systems). Content related to software product strategy, release planning, SaaS engineering models, and economic decision-making is included when explicitly tied to the software lifecycle. Excluded are videos focused solely on hardware engineering, general computer science theory without connection to software engineering practice, pure programming syntax tutorials without engineering context, general technology news, or business topics unrelated to software system development and management.

                    Task:
                    Given the TITLE and DESCRIPTION of a YouTube video, determine whether the video is related to Software Engineering education.

                    Input:
                    TITLE: {title}
                    DESCRIPTION: {description}

                    Output rules:
                    - Respond with ONLY one word: True if related or False if not related.
                    - Do NOT explain, output anything else, add punctuation, or add additional words with your answer.
                    """
        }
    ]

    return instruction