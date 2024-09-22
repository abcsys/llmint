name = "APPLY"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Apply a function to the values of a source field",
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
                "function_name": {
                    "type": "string",
                    "description": "Function to apply",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "function_name", "reasoning"],
        },
    }
}


def func(source_field, target_field, function_name, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, '
            f'transformation: APPLY {source_field} {function_name}}}', reasoning)
