name = "RENAME"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Rename a source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "reasoning"],
        },
    }
}


def func(source_field, target_field, reasoning):
    return (
        f'{{from: {source_field}, to: {target_field}, '
        f'transformation: RENAME {source_field} TO {target_field}}}', reasoning)
