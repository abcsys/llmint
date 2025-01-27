from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "APPLY"
description = "Apply a function to the values of a source field"
properties = {
    "target_field": (str, "Field from the target schema"),
    "function": (str, "An expression involving source schema field(s) to apply, "
                      "replace any spaces in the schema fields with underscores"),
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


def func(target_field, function, reasoning=None):
    return Map(source_field=None,
               target_field=target_field,
               transformation=f'APPLY {function}',
               reasoning=reasoning)
