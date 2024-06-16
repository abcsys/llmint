model = "gpt-4o"
temperature = 0.0
seed = 42

tools = [
    # schema match
    "llmint.map.stl.schema.match",
    # field transformation
    "llmint.map.stl.field.add",
    "llmint.map.stl.field.cast",
    "llmint.map.stl.field.copy",
    "llmint.map.stl.field.default",
    "llmint.map.stl.field.delete",
    "llmint.map.stl.field.rename",
    "llmint.map.stl.field.missing",
    # value transformation
    "llmint.map.stl.value.apply",
    # "llmint.map.stl.value.gen",
    "llmint.map.stl.value.link",
    "llmint.map.stl.value.scale",
    "llmint.map.stl.value.shift",
]
