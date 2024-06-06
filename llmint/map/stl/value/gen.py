name = "GEN"
schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": "Describes the equation needed to convert from source to target values",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "target_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "conversion_equation": {
                    "type": "string",
                    "description": "Mathematical equation used in conversion. "
                                   "Let x be the source value and y be the target value.",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "conversion_equation", "reasoning"],
        },
    }
}
