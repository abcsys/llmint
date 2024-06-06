name = "SHIFT"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Shift the value of a source field",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field from the source schema",
                },
                "target_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "value": {
                    "type": "string",
                    "description": "Value to shift the source field by",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "value", "reasoning"],
        },
    }
}


def func(source_field, target_field, value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, '
            f'transformation: SHIFT {source_field} BY {value}}}', reasoning)
