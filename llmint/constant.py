import os
import sys
import yaml

LLMINT_DIR = os.path.join(os.path.expanduser("~"), ".llmint")
LLMINT_CONFIG_FILE = os.path.join(LLMINT_DIR, "config.yaml")
LLMINT_SOURCE = os.path.dirname(os.path.abspath(__file__))

try:
    with open(LLMINT_CONFIG_FILE, "r") as f:
        LLMINT_CONFIG = yaml.load(f, Loader=yaml.SafeLoader)
except FileNotFoundError:
    print(f"Config file not found at {LLMINT_CONFIG_FILE}")
    sys.exit(1)
