import torch
import pandas as pd
from math import ceil
from tqdm import tqdm
from config import CONFIG
from transformers import pipeline
from logger import get_logger
from prompts import prepare_prompts, prepare_data
from utils import ensure_file, load_existing_ids, get_instruction, extract_label

# Main
def main():
    logger = get_logger()
    output_file_path = ensure_file("data/classification_results.csv", columns=["id", "result"])
    existing_ids = load_existing_ids(output_file_path)
    instruction = get_instruction()
    df = pd.read_csv("data/video_metadata.csv", engine="python")
    videos = prepare_data(df, existing_ids)[:12]

    logger.info("Torch version: %s", torch.__version__)
    logger.info("Using model: %s", CONFIG.MODEL_ID)
    logger.info(
        "CUDA available: %s | GPUs: %s",
        torch.cuda.is_available(),
        torch.cuda.device_count(),
    )

    print(f"Total videos     : {len(df)}")
    print(f"Processing videos: {len(videos)}")
    if not videos:
        return

    pipe = pipeline(
        CONFIG.MODEL_TYPE,
        model=CONFIG.MODEL_ID,
        dtype=CONFIG.DTYPE,
        device_map=CONFIG.DEVICE_MAP,
        return_full_text=CONFIG.RETURN_FULL_TEXT,
    )
    
    # Batched inference
    # fix decoder-only padding
    pipe.tokenizer.padding_side = "left"
    pipe.tokenizer.pad_token = pipe.tokenizer.eos_token
    
    num_batches = ceil(len(videos) / CONFIG.BATCH_PROMPTS)
    
    for i in tqdm(range(num_batches), desc="Processing batches"):
        start = i * CONFIG.BATCH_PROMPTS
        end = start + CONFIG.BATCH_PROMPTS
        
        batch_prompts = prepare_prompts(videos[start:end], instruction)
        outputs = pipe(
        	batch_prompts,
        	batch_size=CONFIG.BATCH_SIZE
    	)

        for idx, out in enumerate(outputs):
            result = out[0]['generated_text'].split('assistantfinal')
            if(len(result)<2):
                continue
            else:
                label = extract_label(result[-1])
                with open(output_file_path, "a") as file:
                    file.write(f"{videos[start+idx]['id']},{label}\n")

# Entry
if __name__ == "__main__":
    main()