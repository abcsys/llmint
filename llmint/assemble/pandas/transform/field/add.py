import re
from pandas import Series

from llmint.map.function import Map


def func(mapping: Map):
    col_type = re.search(r'TYPE (\w+)', mapping.transformation).group(1)
    
    return lambda df: Series([], name=mapping.target_field, dtype=col_type)
