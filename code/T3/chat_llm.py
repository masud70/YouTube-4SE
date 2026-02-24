import torch
import pandas as pd
from math import ceil
from tqdm import tqdm
from config import CONFIG
from logger import get_logger
from prompts import prepare_data
from messages import get_messages
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import ensure_file, load_existing_ids, extract_label

# Main
def main():
    logger = get_logger()
    output_file_path = ensure_file("data/classification_results.csv", columns=["id", "result"])
    existing_ids = load_existing_ids(output_file_path)
    df = pd.read_json("input/200_random_videos_2302.json", orient="records")
    videos = prepare_data(df, existing_ids)

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

    tokenizer = AutoTokenizer.from_pretrained(CONFIG.MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        CONFIG.MODEL_ID,
        torch_dtype=CONFIG.DTYPE,
        device_map=CONFIG.DEVICE_MAP,
    )

    tokenizer.padding_side = "left"
    tokenizer.pad_token = tokenizer.eos_token
    
    # Batched inference
    num_batches = ceil(len(videos) / CONFIG.BATCH_PROMPTS)
    
    for i in tqdm(range(num_batches), desc="Processing batches"):
        start = i * CONFIG.BATCH_PROMPTS
        end = start + CONFIG.BATCH_PROMPTS

        batch_videos = videos[start:end]
        inputs = []
        
        for video in batch_videos:
            messages = get_messages(count=CONFIG.NUM_EXAMPLES)
            messages.append(
                {
                    "role": "user",
                    "content": f"TITLE: {video['title']}\nDESCRIPTION: {video['description']}"
                }
            )

            prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            inputs.append(prompt)

        model_inputs = tokenizer(
            inputs,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(model.device)

        outputs = model.generate(
            **model_inputs,
            max_new_tokens=CONFIG.MAX_NEW_TOKENS,
            do_sample=False
        )

        generated_tokens = outputs[:, model_inputs["input_ids"].shape[1]:]

        decoded = tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True
        )

        for idx, text in enumerate(decoded):
            label = extract_label(text)
            if label == "INVALID":
                continue

            video_id = batch_videos[idx]["id"]
            with open(output_file_path, "a") as file:
                file.write(f"{video_id},{label}\n")

# Entry
if __name__ == "__main__":
    main()