from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "MISSING"
description = "Indicates that the required target field is impossible to construct from the fields in the source schema"
properties = {
    "target_field": (str, "Field from the target schema"),
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


def func(target_field, reasoning=None):
    return Map(source_field=None,
               target_field=target_field,
               transformation=f'MISSING',
               reasoning=reasoning)
