import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://open.bigmodel.cn/api/paas/v4/")
    MODEL_NAME = os.getenv("MODEL_NAME", "glm-4-flash")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

config = Config()