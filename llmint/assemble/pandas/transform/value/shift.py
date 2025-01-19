import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(df: DataFrame, mapping: Map):
    try:
        shift = float(re.search(r'SHIFT BY (\d*.\d*)', mapping.transformation).group(1))
    except ValueError:
        return df[mapping.source_field].copy()
    
    return df[mapping.source_field] + shift
