from libem.match import function as libem_match

name = "MATCH"
schema = libem_match.schema


def func(source_schema, target_schema):
    return libem_match.func(
        left=source_schema,
        right=target_schema
    ) == "yes"


def output():
    return "MISMATCH"
