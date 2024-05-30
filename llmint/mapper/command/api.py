import llmint.mapper.command.model as model
import llmint.mapper.command.util as util

def map_with_reasoning(file, include_reasoning=False):
    """ Return the mapping for a given source schema and target schema.
    
    Args:
        source_schema (string): source schema
        target_schema (string): target schema
        include_reasoning (boolean): whether or not to print model's reasoning in the output
    """
    input_schemas = util.from_yaml(file)
    source_schema = str(input_schemas[0])
    target_schema = str(input_schemas[1])
    
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)
    
    response = model.call(messages)
    util.print_responses(response, include_reasoning)
    
def mapping_with_info(source_schema, target_schema):
    """ Return the mapping for a given source schema and target schema.
    
    Args:
        source_schema (string): source schema
        target_schema (string): target schema
    """
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)
    
    response_info = model.call(messages)
    util.print_responses(response_info[0])
    return 

def map(source_schema, target_schema, include_reasoning=False, include_info=False):    
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)

    # remove reasoning from output
    response_info = model.call(messages)
    if not include_reasoning:
        for i in range(len(response_info[0])):
            response_info[0][i] = response_info[0][i][0]
    
    if include_info:
        return response_info
    return response_info[0]