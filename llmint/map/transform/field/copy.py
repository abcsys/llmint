from llmint.map.function import Map


name = "COPY"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Directly copies data from the source field "
                       "to the target field without any transformation..",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field in the source schema",
                },
                "target_field": {
                    "type": "string",
                    "description": "Field in the target schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "field_type", "reasoning"],
        },
    }
}


def func(source_field, target_field, reasoning):
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'COPY',
               reasoning=reasoning)
