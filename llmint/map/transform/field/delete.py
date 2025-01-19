from llmint.map.function import Map


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
    return Map(source_field=source_field,
               target_field=None,
               transformation=f'DELETE',
               reasoning=reasoning)
