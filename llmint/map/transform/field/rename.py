from llmint.map.function import Map


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
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'RENAME TO {target_field}',
               reasoning=reasoning)
