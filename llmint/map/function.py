from llmint.core import model
from llmint.map import prompt, parameter

def map(source_schema, target_schema):
    mappings = model.call(
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
    return mappings
