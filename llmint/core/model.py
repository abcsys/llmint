import os

import llmint

os.environ.setdefault(
    "OPENAI_API_KEY",
    llmint.LLMINT_CONFIG.get("OPENAI_API_KEY", "")
)

from libem.core.model import call
_ = call
