from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "SCALE"
description = "Scale the value of a source field"
properties = {
    "source_field": (str, "Field from the source schema"),
    "target_field": (str, "Field from the target schema"),
    "factor": (str, "Factor to multiply the source field by"),
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


def func(source_field, target_field, factor, reasoning=None):
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'SCALE BY {factor}',
               reasoning=reasoning)
