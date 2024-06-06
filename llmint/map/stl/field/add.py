name = "ADD"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Add an optional target field",
        "parameters": {
            "type": "object",
            "properties": {
                "target_field": {
                    "type": "string",
                    "description": "Optional field in the target schema",
                },
                "field_type": {
                    "type": "string",
                    "description": "The type of the field to be added",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "field_type", "reasoning"],
        },
    }
}


def func(target_field, field_type, reasoning):
    return (f'{{from: None, to: {target_field}, '
            f'transformation: ADD {target_field} TYPE {field_type}}}', reasoning)
