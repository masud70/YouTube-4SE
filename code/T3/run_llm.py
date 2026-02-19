import copy
import torch
import logging
import pandas as pd
from math import ceil
from tqdm import tqdm
from datetime import date
from transformers import pipeline
from logger import get_logger
from utils import ensure_file, extract_json, build_prompt

logger = get_logger()
file_path = ensure_file("data/classification_results.csv", columns=["id", "result"])

# Config
MODEL_ID = "openai/gpt-oss-20b"
BATCH_SIZE = 6
MAX_NEW_TOKENS = 128
BATCH_PROMPTS = 12

# Main
def main():
    pipe = pipeline(
        "text-generation",
        model=MODEL_ID,
        dtype="auto",
        device_map="auto",
        return_full_text=False,
    )

    logging.info("Torch version: %s", torch.__version__)
    logging.info(
        "CUDA available: %s | GPUs: %s",
        torch.cuda.is_available(),
        torch.cuda.device_count(),
    )

    # Load processed IDs
    try:
        existing_ids = set(pd.read_csv(output_file)["id"].astype(str))
    except Exception:
        existing_ids = set()

    print(f"Already processed {len(existing_ids)} videos.")

    # YOUR COMMANDS (unchanged)
    commands = []

    # Load metadata
    df = pd.read_csv("data/video_metadata.csv", engine="python")

    prompts = []

    for _, row in df.iterrows():
        vid = str(row["id"])
        if vid in existing_ids:
            continue

        p = build_prompt(
                copy.deepcopy(commands) + [{
                    "role": "user",
                    "content": (
                        f"id: {row['id']}, "
                        f"title: {row['title']}, "
                        f"description: {row['description']}"
                    )
                }]
            )
        prompts.append(p)

    print(f"Total videos     : {len(df)}")
    print(f"Processing videos: {len(prompts)}")

    if not prompts:
        return

    # Batched inference
    # fix decoder-only padding
    pipe.tokenizer.padding_side = "left"
    pipe.tokenizer.pad_token = pipe.tokenizer.eos_token
    
    results = []
    num_batches = ceil(len(prompts) / BATCH_PROMPTS)
    
    for i in tqdm(range(num_batches), desc="Processing batches"):
        start = i * BATCH_PROMPTS
        end = start + BATCH_PROMPTS
        
        batch_prompts = prompts[start:end]
        outputs = pipe(
        	batch_prompts,
        	batch_size=BATCH_SIZE
    	)

        for out in outputs:
            text = out[0]["generated_text"]
            parsed = extract_json(text)
            if parsed and "id" in parsed and "result" in parsed:
                results.append(parsed)

        if len(results):
            df_out = pd.DataFrame(results)
            df_out.to_csv(output_file, mode="a", header=False, index=False)
            results = []

# Entry
if __name__ == "__main__":
    main()