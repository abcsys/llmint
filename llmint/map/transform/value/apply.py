from llmint.map.function import Map


name = "APPLY"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Apply a function to the values of a source field",
        "parameters": {
            "type": "object",
            "properties": {
                "target_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "function": {
                    "type": "string",
                    "description": "An expression involving source schema field(s) to apply, "
                                   "replace any spaces in the schema fields with underscores",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "function", "reasoning"],
        },
    }
}


def func(target_field, function, reasoning):
    return Map(source_field=None,
               target_field=target_field,
               transformation=f'APPLY {function}',
               reasoning=reasoning)
