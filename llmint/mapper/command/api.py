import llmint.mapper.command.model as model
import llmint.mapper.command.util as util

def mapping_formatted_map(file, include_reasoning=False):
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

def map(source_schema, target_schema):    
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)

    # remove reasoning from output
    response = model.call(messages)
    """
    for i in range(len(response)):
        response[i] = response[i][0]
    """
        
    # return a list of mappings
    return response