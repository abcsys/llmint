from pydantic import BaseModel

from llmint.core import model
from llmint.map import prompt, parameter


class Map(BaseModel):
    source_field: str | None
    target_field: str
    transformation: str
    reasoning: str | None


def map(source_schema, target_schema):
    output = model.call(
        prompt=[
            {"role": "system", "content": prompt.system},
            {"role": "user", "content": prompt.user.format(
                source_schema=source_schema,
                target_schema=target_schema,
            )},
        ],
        tools=parameter.tools,
        model=parameter.model,
        temperature=parameter.temperature,
        seed=parameter.seed,
        max_model_call=1,  # only one model call
    )["tool_outputs"]
    
    # process the mappings
    mappings = []
    for mapping in output:
        for _, mapping in mapping.items():
            mappings.append(mapping)
    
    return mappings
