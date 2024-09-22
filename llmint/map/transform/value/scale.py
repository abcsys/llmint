name = "SCALE"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Scale the value of a source field",
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
                "factor": {
                    "type": "string",
                    "description": "Factor to multiply the source field by",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "factor", "reasoning"],
        },
    }
}


def func(source_field, target_field, factor, reasoning):
    return (
        f'{{from: {source_field}, to: {target_field}, '
        f'transformation: SCALE {source_field} BY {factor}}}', reasoning)
