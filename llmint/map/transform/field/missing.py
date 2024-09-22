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
    return (f'{{from: None, to: {target_field}, '
            f'transformation: MISSING {target_field}}}', reasoning)
