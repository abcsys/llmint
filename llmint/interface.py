from llmint.map.match import func as match_func
from llmint.map.function import map as map_func


def match(*args, **kwargs):
    return match_func(*args, **kwargs)


def map(*args, **kwargs):
    return map_func(*args, **kwargs)
