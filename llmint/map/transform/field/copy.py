from libem.core.util import create_json_schema

from llmint.map.function import Map
from llmint.map.parameter import reasoning
from llmint.map.prompt import reasoning_prompt


name = "COPY"
description = "Directly copies data from the source field to the target field without any transformation."
properties = {
    "source_field": (str, "Field in the source schema"),
    "target_field": (str, "Field in the target schema"),
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



def func(source_field, target_field, reasoning=None):
    return Map(source_field=source_field,
               target_field=target_field,
               transformation=f'COPY',
               reasoning=reasoning)
