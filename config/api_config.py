import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    SHOPIFY_WEBHOOK_SECRET: str = os.getenv("SHOPIFY_WEBHOOK_SECRET", "")
