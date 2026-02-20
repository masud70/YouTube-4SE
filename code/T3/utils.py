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


def get_instruction():
    instruction = [
        {
            "role": "SYSTEM",
            "content": """
                        You are a strict binary classifier for Software Engineering educational content.

                        Definition:
                        This study considers YouTube videos that contribute to Software Engineering (SE) education worldwide, focusing on content that supports the systematic and disciplined development, operation, and maintenance of software systems. In this work, Software Engineering includes the core phases of the Software Development Life Cycle (SDLC), such as requirements engineering, system design, implementation, testing, deployment, and maintenance, as well as related technical and managerial practices. The scope covers programming concepts when presented in the context of software construction, code quality, design patterns, version control, debugging, refactoring, software architecture, DevOps practices, project management, documentation, and quality assurance. Research-oriented topics—such as empirical software engineering, software metrics, AI for software engineering, software engineering for AI, and software security—are included when directly connected to improving software development processes or systems. Recognizing software as a product, the definition also includes content on product management, release strategies, and SaaS models when clearly tied to the software lifecycle. Excluded are videos focused solely on hardware engineering, purely theoretical topics unrelated to software systems, general technology news without educational depth, isolated coding exercises without engineering context, or business discussions not explicitly connected to software development.

                        Task:
                        Given the TITLE and DESCRIPTION of a YouTube video, determine whether the video is related to Software Engineering education.

                        Include videos that teach or explain methods, practices, tools, research, or strategies related to building, managing, or evolving software systems.

                        Exclude videos focused only on:
                        - Pure programming syntax without engineering context
                        - Hardware engineering
                        - General technology news
                        - Pure mathematics unrelated to software systems
                        - Business topics not directly tied to software development
                        - Entertainment content unrelated to software engineering

                        Output rules:
                        Respond with ONLY one word: True or False
                        True  -> if related.
                        False -> if not related.
                        Do NOT explain your answer.
                        Do NOT output anything else.
                        Do NOT add punctuation.
                        Do NOT add additional words.

                        TITLE: {title}
                        DESCRIPTION: {description}
                    """
        }
    ]

    return instruction