from pandas import Series

from llmint.map.function import Map


def func(mapping: Map):
    return lambda df: Series(df[mapping.source_field], name=mapping.target_field)
