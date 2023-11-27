import os
import json
import yaml

from openai import OpenAI, ChatCompletion
from field_transformation.functions import addFunction, changeTypeFunction, deleteFunction, renameFunction, setDefaultFunction, applyFuncFunction, mapFunction, scaleFunction, shiftFunction, combineFunction,   splitFunction

from util.util import chat_completion_request, pretty_print_conversation, call_fn

add = {
        "type": "function",
        "function": {
            "name": "addFunction",
            "description": "Returns the mapping operator between a source and target schema field where the field is not present in the source schema but is present in the target schema",
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
            "description": "Returns the mapping operator between a source and target schema field with different types",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source record",
                    },
                    "target_field": {
                        "type": "string", 
                        "description": "A singular field name from the target record corresponding to the source_field",
                    },
                    "source_type": {
                        "type": "string", 
                        "description": "The source type of the field name",
                    },
                    "target_type": {
                        "type": "string", 
                        "description": "The target type of the field name",
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
            "description": "Returns the mapping operator between a source and target schema field where the field is present in the source schema but not in the target schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name which is present in the source schema but not present in the target schema",
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
            "description": "Returns the mapping operator between a source and target schema field with different names",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source record",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target record corresponding to the source_field",
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
            "description": "Returns the mapping operator that sets the default value of a target schema's field",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source record",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "A singular field name from the target record corresponding to the source_field",
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
            "description": "Returns the mapping operator for a field who's target value is achieved by applying the function_name to the source value",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_name": {
                        "type": "string",
                        "description": "A singular field name that has different values between the source and target schema",
                    },
                    "function_name": {
                        "type": "string",
                        "description": "A function name which the field's value in the source schema should be processed by to match the value in the target schema",
                    },
                },
                "required": ["field_name", "function_name"],
            },
        }
    }

map = {
        "type": "function",
        "function": {
            "name": "mapFunction",
            "description": "Returns the mapping operator for a field who's value is of different types between the source and target schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "A singular field name that has different values between the source and target schema",
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
                "required": ["field", "old_value", "new_value"],
            },
        }
    }

scale = {
        "type": "function",
        "function": {
            "name": "scaleFunction",
            "description": "Returns the mapping operator for a field who's value is of different scale between the source and target schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "A singular field name that has different values between the source and target schema",
                    },
                    "factor": {
                        "type": "string",
                        "description": "The factor by which the field's value in the source schema should be scaled by to match the value in the target schema",
                    },
                },
                "required": ["field", "factor"],
            },
        }
    }

shift = {
        "type": "function",
        "function": {
            "name": "shiftFunction",
            "description": "Returns the mapping operator for a field who's value is shifted between the source and target schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "A singular field name that has different values between the source and target schema",
                    },
                    "value": {
                        "type": "string",
                        "description": "The value by which the field's value in the source schema should be shifted by to match the value in the target schema",
                    },
                },
                "required": ["field", "value"],
            },
        }
    }

combine = {
        "type": "function",
        "function": {
            "name": "combineFunction",
            "description": "Returns the mapping operator between a 2 source fields and 1 target fields where the target field is a combination of the source fields",
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
            "description": "Returns the mapping operator between a source and target schema fields where the target fields are split from the source fields",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "A singular field name from the source schema",
                    },
                    "new_field_1": {
                        "type": "string",
                        "description": "A new target field name split from the source field name",
                    },
                    "new_field_2": {
                        "type": "string",
                        "description": "A new target field name split from the source field name",
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

tools = [add, changeType, delete, rename, set_default, apply_func, map, scale, shift, combine, split]

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