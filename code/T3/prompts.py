import copy
from tqdm import tqdm

def prepare_prompts(video_df, existing_ids, instruction):
    prompts = []
    for _, row in tqdm(video_df.iterrows()):
        id = str(row['id'])
        if id in existing_ids:
            continue
        else:
            prompt = build_prompt(
                copy.deepcopy(instruction) + [
                    {
                        "role": "USER",
                        "content": (
                            f"TITLE: {row['id']}, "
                            f"DESCRIPTION: {row['description']}"
                        )
                    }
                ]
            )
            prompts.append(prompt)
    
    return prompts


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