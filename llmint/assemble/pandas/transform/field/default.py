import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(df: DataFrame, mapping: Map):
    default_val = re.search(r'DEFAULT TO (.*)', mapping.transformation).group(1)
    
    return Series([default_val] * len(df), name=mapping.target_field)
