name = "DELETE"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Delete a source field",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field from the source schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "reasoning"],
        },
    }
}


def func(source_field, reasoning):
    return (f'{{from: {source_field}, to: None, '
            f'transformation: DELETE {source_field}}}', reasoning)
