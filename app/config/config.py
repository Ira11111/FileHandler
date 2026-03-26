import os
from functools import lru_cache

import yaml


REPORTS_DIR = os.path.join(os.getcwd(), "data", "reports")
UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")

class Config:
    def __init__(self, data_dict):
        if getattr(self, "_initialized", False):
            return

        for key, value in data_dict.items():
            if isinstance(value, dict):
                setattr(self, key, Config(value))
            else:
                setattr(self, key, value)

        self._initialized = True


@lru_cache(maxsize=1)
def load_config(filepath: str = "config.yaml") -> Config:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config(data)
