from llmint.core import model
from llmint.map import prompt, parameter


def map(source_schema, target_schema):
    model_outputs, tool_outputs = model.call(
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
        verbose=parameter.verbose,
        max_model_call=1,  # only one model call
        return_tool_outputs=True,
    )
    _, mappings = model_outputs, tool_outputs
    return mappings
