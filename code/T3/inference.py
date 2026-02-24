from config import CONFIG
from transformers import AutoTokenizer, AutoModelForCausalLM

def inference():
    tokenizer = AutoTokenizer.from_pretrained(CONFIG.MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        CONFIG.MODEL_ID,
        torch_dtype=CONFIG.DTYPE,
        device_map=CONFIG.DEVICE_MAP,
    )

    tokenizer.padding_side = "left"
    tokenizer.pad_token = tokenizer.eos_token