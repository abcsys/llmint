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
    return (f'{{from: {source_field}, to: {target_field}, '
            f'transformation: COPY}}', reasoning)
