import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(df: DataFrame, mapping: Map):
    return Series(df[mapping.source_field], name=mapping.target_field)
