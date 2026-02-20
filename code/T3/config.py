class CONFIG:
    MODEL_TYPE = "text-generation"
    MODEL_ID = "openai/gpt-oss-20b"
    DTYPE = "auto",
    DEVICE_MAP = "auto",
    RETURN_FULL_TEXT = False,
    
    BATCH_SIZE = 6
    MAX_NEW_TOKENS = 64
    BATCH_PROMPTS = 12