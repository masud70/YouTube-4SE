import torch
import pandas as pd
from math import ceil
from tqdm import tqdm
from transformers import pipeline
from logger import get_logger
from prompts import prepare_prompts
from utils import ensure_file, load_existing_ids, get_instruction

# Config
MODEL_ID = "openai/gpt-oss-20b"
BATCH_SIZE = 6
MAX_NEW_TOKENS = 64
BATCH_PROMPTS = 12

# Main
def main():
    logger = get_logger()
    file_path = ensure_file("data/classification_results.csv", columns=["id", "result"])
    existing_ids = load_existing_ids(file_path)
    instruction = get_instruction()
    df = pd.read_csv("data/video_metadata.csv", engine="python")
    prompts = prepare_prompts(df, existing_ids, instruction)

    logger.info("Torch version: %s", torch.__version__)
    logger.info("Using model: %s", MODEL_ID)
    logger.info(
        "CUDA available: %s | GPUs: %s",
        torch.cuda.is_available(),
        torch.cuda.device_count(),
    )

    print(f"Total videos     : {len(df)}")
    print(f"Processing videos: {len(prompts)}")
    if not prompts:
        return

    pipe = pipeline(
        "text-generation",
        model=MODEL_ID,
        dtype="auto",
        device_map="auto",
        return_full_text=False,
    )
    
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

        print(outputs)
        print(outputs[0]['generated_text'][-1])

# Entry
if __name__ == "__main__":
    main()