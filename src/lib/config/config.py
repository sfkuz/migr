import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default: Optional[str] = None, optional: bool = False) -> Optional[str]:
    value = os.getenv(key)

    if value is not None:
        return value

    if default is not None:
        return default

    if optional:
        return None

    raise ValueError(f"Environment variable '{key}' is required but not set.")

DATABASE_URL = get_env("DATABASE_URL")
