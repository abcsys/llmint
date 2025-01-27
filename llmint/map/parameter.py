model = "gpt-4o"
temperature = 0.0
seed = 42

tools = [
    # schema match
    "llmint.map.match",
    # field transformation
    "llmint.map.transform.field.add",
    # "llmint.map.transform.field.cast",
    "llmint.map.transform.field.copy",
    "llmint.map.transform.field.default",
    # "llmint.map.transform.field.delete",
    # "llmint.map.transform.field.rename",
    "llmint.map.transform.field.missing",
    # value transformation
    "llmint.map.transform.value.apply",
    # "llmint.map.transform.value.gen",
    # "llmint.map.transform.value.link",
    "llmint.map.transform.value.scale",
    "llmint.map.transform.value.shift",
]

reasoning = False
