import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(df: DataFrame, mapping: Map):
    col_type = re.search(r'TYPE (\w+)', mapping.transformation).group(1)
    
    return Series([], name=mapping.target_field, dtype=col_type)
