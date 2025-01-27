from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "LINK"
description = "Create a mapping between a value in the source field to a value in the target field, usually for enum type values"
properties = {
    "source_field": (str, "Field from the source schema"),
    "target_field": (str, "Field from the target schema"),
    "old_value": (str, "Source field value"),
    "new_value": (str, "Target field value"),
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

def func(source_field, target_field, old_value, new_value, reasoning=None):
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'LINK {source_field} "{old_value}" TO "{new_value}"',
               reasoning=reasoning)