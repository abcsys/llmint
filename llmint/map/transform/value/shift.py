from llmint.map.function import Map


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
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'SHIFT BY {value}',
               reasoning=reasoning)
