name = "LINK"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Create a mapping between a value in the source field to a value in the target field, usually for enum type values",
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
                "old_value": {
                    "type": "string",
                    "description": "Source field value",
                },
                "new_value": {
                    "type": "string",
                    "description": "Target field value",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "old_value", "new_value", "reasoning"],
        },
    }
}

def func(source_field, target_field, old_value, new_value, reasoning):
    return (
    f'{{from: {source_field}, to: {target_field}, '
    f'transformation: LINK {source_field} "{old_value}" TO "{new_value}"}}',
    reasoning)