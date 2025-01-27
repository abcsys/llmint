import re
from pandas import Series

from llmint.map.function import Map


def func(mapping: Map):
    default_val = re.search(r'DEFAULT TO (.*)', mapping.transformation).group(1)
    
    return lambda df: Series([default_val] * len(df), name=mapping.target_field)
