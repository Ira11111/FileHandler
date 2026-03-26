import yaml


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



def load_config(filepath: str = "config.yaml") -> Config:
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config(data)
