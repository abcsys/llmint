import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(df: DataFrame, mapping: Map):
    try:
        scale = float(re.search(r'SCALE BY (\d*.\d*)', mapping.transformation).group(1))
    except ValueError:
        return df[mapping.source_field].copy()
    
    return df[mapping.source_field] * scale
