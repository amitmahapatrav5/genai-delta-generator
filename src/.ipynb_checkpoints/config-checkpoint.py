from pathlib import Path
from yaml import safe_load

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
config = safe_load(open(CONFIG_PATH))