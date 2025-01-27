import re

from llmint.map.function import Map


def func(mapping: Map):
    try:
        shift = float(re.search(r'SHIFT BY (\d*.\d*)', mapping.transformation).group(1))
    except ValueError:
        return lambda df: df[mapping.source_field].copy()
    
    return lambda df: df[mapping.source_field] + shift
