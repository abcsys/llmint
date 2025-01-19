from llmint.map.function import Map


name = "ADD"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Add an optional target field",
        "parameters": {
            "type": "object",
            "properties": {
                "target_field": {
                    "type": "string",
                    "description": "Optional field in the target schema",
                },
                "field_type": {
                    "type": "string",
                    "description": "The type of the field to be added",
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


def func(target_field, field_type, reasoning):
    return Map(source_field=None, 
               target_field=target_field, 
               transformation=f'ADD {target_field} TYPE {field_type}', 
               reasoning=reasoning)
