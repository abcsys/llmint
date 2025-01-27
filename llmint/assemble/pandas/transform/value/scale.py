import re

from llmint.map.function import Map


def func(mapping: Map):
    try:
        scale = float(re.search(r'SCALE BY (\d*.\d*)', mapping.transformation).group(1))
    except ValueError:
        return lambda df: df[mapping.source_field].copy()
    
    return lambda df: df[mapping.source_field] * scale
