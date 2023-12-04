import os
import json
import yaml

from openai import OpenAI, ChatCompletion
from field_transformation.functions import (addFunction, 
                                            changeTypeFunction, 
                                            deleteFunction, 
                                            renameFunction, 
                                            setDefaultFunction, 
                                            applyFuncFunction, 
                                            mapFunction, 
                                            scaleFunction, 
                                            shiftFunction, 
                                            combineFunction, 
                                            splitFunction, 
                                            missingFunction)

from util.util import chat_completion_request, pretty_print_conversation, call_fn

add = {
        "type": "function",
        "function": {
            "name": "addFunction",
            "description": "Returns a mapping operator between a source and target schema, where an effective translation from source to target schema consists of adding a field to the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name which is not present in the source schema but is present in the target schema",
                    },
                    "field_type": {
                        "type": "string", 
                        "description": "The type of the field to be added",
                    },
                },
                "required": ["target_field", "field_type"],
            },
        }
    }

changeType = {
        "type": "function",
        "function": {
            "name": "changeTypeFunction",
            "description": "Returns a mapping operator between a source and target schema, where an effective tranlsation from source to target schema consists of changing the type of a source field",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string", 
                        "description": "A singular field name from the target schema",
                    },
                    "source_type": {
                        "type": "string", 
                        "description": "The type of the source field",
                    },
                    "target_type": {
                        "type": "string", 
                        "description": "The type of the target field",
                    },
                },
                "required": ["source_field", "target_field", "source_type", "target_type"],
            },
        }
    }

delete = {
        "type": "function",
        "function": {
            "name": "deleteFunction",
            "description": "Returns a mapping operator between a source and target schema, where an effective translation from source to target schema consists of deleting a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                },
                "required": ["source_field"],
            },
        }
    }

rename = {
        "type": "function",
        "function": {
            "name": "renameFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of renaming a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                },
                "required": ["source_field", "target_field"],
            },
        }
    }

set_default = {
        "type": "function",
        "function": {
            "name": "setDefaultFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of setting a new default value for a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                    "default_value": {
                        "type": "string",
                        "description": "The default value of the given target schema's field",
                    },
                },
                "required": ["source_field", "target_field", "default_value"],
            },
        }
    }

apply_func = {
        "type": "function",
        "function": {
            "name": "applyFuncFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of applying a function to the values of a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                    "function_name": {
                        "type": "string",
                        "description": "The name of the function to apply to the values of the source field in order to achieve the values of the target field",
                    },
                },
                "required": ["source_field", "target_field", "function_name"],
            },
        }
    }

map = {
        "type": "function",
        "function": {
            "name": "mapFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of defining a mapping between the value of a field from the source schema to a value of a field from the target schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                    "old_value": {
                        "type": "string",
                        "description": "The value of the field in the source schema",
                    },
                    "new_value": {
                        "type": "string",
                        "description": "The value of the field in the target schema",
                    },
                },
                "required": ["source_field", "target_field", "old_value", "new_value"],
            },
        }
    }

scale = {
        "type": "function",
        "function": {
            "name": "scaleFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of scaling the values of a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                    "factor": {
                        "type": "string",
                        "description": "The factor by which the source field's values should be scaled by to match the target field's values",
                    },
                },
                "required": ["source_field", "target_field", "factor"],
            },
        }
    }

shift = {
        "type": "function",
        "function": {
            "name": "shiftFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of shifting the values of a field from the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                    "value": {
                        "type": "string",
                        "description": "The value by which the source field's values should be shifted by to match the target field's values",
                    },
                },
                "required": ["source_field", "target_field", "value"],
            },
        }
    }

combine = {
        "type": "function",
        "function": {
            "name": "combineFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of combining 2 source field names into 1 target field name",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_1": {
                        "type": "string",
                        "description": "A singular field name from the source record",
                    },
                    "field_2": {
                        "type": "string",
                        "description": "A singular field name from the source record",
                    },
                    "new_field": {
                        "type": "string",
                        "description": "A singular field name from the target record that is a combination of field_1 and field_2",
                    },
                    "operation": {
                        "type": "string",
                        "description": "The function to use for combining",
                    },
                },
                "required": ["field_1", "field_2", "new_field", "operation"],
            },
        }
    }

split = {
        "type": "function",
        "function": {
            "name": "splitFunction",
            "description": "Returns the mapping operator between a source and target schema, where an effective translation from source to target schema consists of splitting 1 source field name into 2 target field names",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "new_field_1": {
                        "type": "string",
                        "description": "A singular target field name split from the source field name",
                    },
                    "new_field_2": {
                        "type": "string",
                        "description": "A singular target field name split from the source field name",
                    },
                    "delimiter": {
                        "type": "string",
                        "description": "The delimiter character to split the source field name on",
                    },
                },
                "required": ["source_field", "new_field_1", "new_field_2"],
            },
        }
    }

missing = {
        "type": "function",
        "function": {
            "name": "missingFunction",
            "description": "Returns the mapping operator between a source and target schema, where a field from the target schema is unable to be translated from the information in the source",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target schema",
                    },
                },
                "required": ["target_field"],
            },
        }
    }

tools = [add, 
         changeType, 
         delete, 
         rename, 
         set_default, 
         apply_func, 
         map, 
         scale, 
         shift, 
         combine, 
         split, 
         missing]

# https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial
def tutorial():
    response = ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        # messages = messages,
        functions = tools,
        function_call = 'auto'
    )
    
    json_response = json.loads(response['choices'][0]['message']['function_call']['arguments'])
    return json_response

def from_yaml(filepath):
    """Load a YAML file and return the data."""
    with open(filepath, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)
    
def format_source_target(source, target):
    return "Source Schema: " + source + "\nTarget Schema: " + target

#https://platform.openai.com/docs/guides/function-calling
def documentation_walkthrough(messages):
    # Step 1: send the conversation and available functions to the model
    client = OpenAI(api_key="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")
    
    response = client.chat.completions.create(
        #model="gpt-3.5-turbo-1106",
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools,
        temperature=0,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls 

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "addFunction": addFunction,
            "changeTypeFunction": changeTypeFunction,
            "deleteFunction": deleteFunction,
            "renameFunction": renameFunction,
            "setDefaultFunction": setDefaultFunction,
            "applyFuncFunction": applyFuncFunction,
            "mapFunction": mapFunction,
            "scaleFunction": scaleFunction,
            "shiftFunction": shiftFunction,
            "combineFunction": combineFunction,
            "splitFunction": splitFunction,
            "missingFunction": missingFunction,
        }
        messages.append(response_message) # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        function_responses = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name 
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = call_fn(function_name, function_args)
            function_responses.append(function_response)
            print(function_response)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            ) # extend conversation with function response
        # return function_responses
        print("Token Usage: ", response.usage)
        return function_responses
    
def cookbook():
    chat_response = chat_completion_request(
        # messages,
        tools=tools,
        tool_choice="auto",
    )
    assistant_message = chat_response.json()
    print(chat_response.json()['usage'])
    return assistant_message