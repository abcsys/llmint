name = "DEFAULT"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Set the default of a target field",
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
                "default_value": {
                    "type": "string",
                    "description": "Default value of the target field",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "default_value", "reasoning"],
        },
    }
}


def func(source_field, target_field, default_value, reasoning):
    return (
        f'{{from: {source_field}, to: {target_field}, '
        f'transformation: DEFAULT {target_field} TO {default_value}}}', reasoning)
