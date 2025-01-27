from llmint.map.function import Map


def func(mapping: Map):
    return lambda df: print(f"WARNING: {mapping.target_field} field cannot be automatically converted.")
