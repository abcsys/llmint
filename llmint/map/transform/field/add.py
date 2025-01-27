from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "ADD"
description = "Add an optional target field"
properties = {
    "target_field": (str, "Optional field in the target schema"),
    "field_type": (str, "The type of the field to be added"),
}
if reasoning:
    properties["reasoning"] = (str, reasoning_prompt)

schema = {
    "type": "function",
    "function": {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": create_json_schema(
                **properties
            )["properties"],
            "required": list(properties.keys()),
        }
    }
}


def func(target_field, field_type, reasoning=None):
    return Map(source_field=None, 
               target_field=target_field, 
               transformation=f'ADD {target_field} TYPE {field_type}', 
               reasoning=reasoning)
