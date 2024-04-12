import os
from .function_model import *
from .util.util import *


def map_from_file(file, include_reasoning=False):
    """ Return the mapping for a given source schema and target schema.
    
    source_schema: string representing the source schema
    target_schema: string representing the target schema
    include_reasoning: boolean indicating whether or not to print model's reasoning in the output
    """
    input_schemas = from_yaml(file)
    source_schema = str(input_schemas[0])
    target_schema = str(input_schemas[1])
    
    with open("instructions/llmint_base.txt") as f:
        messages = [{"role": "system",
                    "content": f.read()
                }]
    # STL instructional message sent to the model
    with open("instructions/stl_base.txt") as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })
    # end instructional message sent to the model
    with open("instructions/end_base.txt") as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })  
    messages.append({
        "role": "user",
        "content": format_source_target(source_schema, target_schema)
    })
    
    response = function_model(messages)
    print_responses(response, include_reasoning)

def map(source_schema, target_schema):
    module_dir = os.path.dirname(__file__)
    
    with open(os.path.join(module_dir, 'instructions', 'llmint_base.txt')) as f:
        messages = [{"role": "system",
                    "content": f.read()
                }]
    # STL instructional message sent to the model
    with open(os.path.join(module_dir, 'instructions', 'stl_base.txt')) as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })
    # end instructional message sent to the model
    with open(os.path.join(module_dir, 'instructions', 'end_base.txt')) as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })  
    messages.append({
        "role": "user",
        "content": format_source_target(source_schema, target_schema)
    })
    return function_model(messages)