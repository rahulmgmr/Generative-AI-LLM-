from pathlib import Path

import yaml


DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.yaml")


def load_config(path=DEFAULT_CONFIG_PATH):
    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config
