from llmint.core import util

from llmint.core import model

def map(source_schema,
        target_schema,
        include_reasoning=False,
        include_info=False):
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)

    # remove reasoning from output
    # XXX
    response_info = model.call(messages)
    if not include_reasoning:
        for i in range(len(response_info[0])):
            response_info[0][i] = response_info[0][i][0]

    if include_info:
        return response_info
    return response_info[0]


