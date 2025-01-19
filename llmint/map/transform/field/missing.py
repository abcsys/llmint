from llmint.map.function import Map


name = "MISSING"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Indicates that the required target field is impossible to construct from the fields in the source schema",
        "parameters": {
            "type": "object",
            "properties": {
                "target_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "reasoning"],
        },
    }
}


def func(target_field, reasoning):
    return Map(source_field=None,
               target_field=target_field,
               transformation=f'MISSING',
               reasoning=reasoning)
