from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt

name = "GEN"
description = "Describes the equation needed to convert from source to target values"
properties = {
    "source_field": (str, "Field from the target schema"),
    "target_field": (str, "Field from the target schema"),
    "conversion_equation": (str, "Mathematical equation used in conversion. "
                                 "Let x be the source value and y be the target value."),
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
