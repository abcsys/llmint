from llmint.map.function import Map


name = "CAST"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Change the type of the source field",
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
                "source_type": {
                    "type": "string",
                    "description": "Source field type",
                },
                "target_type": {
                    "type": "string",
                    "description": "Target field type",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "source_type", "target_type", "reasoning"],
        },
    }
}


def func(source_field, target_field, source_type, target_type, reasoning):
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'CAST FROM {source_type} TO {target_type}',
               reasoning=reasoning)
