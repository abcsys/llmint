import json
from openai import OpenAI
from util.util import *
from field_transformation.functions import (addOptionalFunction, 
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

add_optional = {
        "type": "function",
        "function": {
            "name": "addOptionalFunction",
            "description": "Add an optional field if the target schema contains an optional field that is not in the source schema. Only add optional fields",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_field": {
                        "type": "string",
                        "description": "Optional field in the target schema",
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
            "description": "Change the type of the field if the target schema contains a field with a different type",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string", 
                        "description": "Field from the target schema",
                    },
                    "source_type": {
                        "type": "string", 
                        "description": "Source field type",
                    },
                    "target_type": {
                        "type": "string", 
                        "description": "Target field type",
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
            "description": "Delete a source field if the target schema does not contain a correlating field",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
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
            "description": "Rename a source field if the target schema contains a correlating field with a different name",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
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
            "description": "Set the default of a field if the target schema contains a field with a different default type than the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "default_value": {
                        "type": "string",
                        "description": "Default value of the target field",
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
            "description": "Apply a function to the values of a source field if the target field's values are a function of the source field's values",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "function_name": {
                        "type": "string",
                        "description": "Function to apply",
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
            "description": "Create a mapping between a value in the source field to a value in the target field, usually for enum type values",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "old_value": {
                        "type": "string",
                        "description": "Source field value",
                    },
                    "new_value": {
                        "type": "string",
                        "description": "Target field value",
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
            "description": "Scale the value of a source field if the target field's values are some factor of the source field's values",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "factor": {
                        "type": "string",
                        "description": "Factor to multiply the source field by",
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
            "description": "Shift the value of a source field if the target field's values are some shifted value of the source field's values",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to shift the source field by",
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
            "description": "Combine 2 source fields if the target field is some combination of the source fields",
            "parameters": {
                "type": "object",
                "properties": {
                    "field_1": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "field_2": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "new_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "operation": {
                        "type": "string",
                        "description": "Function ",
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
            "description": "Split the source field if the target fields are some split of the source field",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the source schema",
                    },
                    "new_field_1": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "new_field_2": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "delimiter": {
                        "type": "string",
                        "description": "Delimiter to split the source field on",
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
            "description": "Indicates that the target field is impossible to construct from the fields in the source schema",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                },
                "required": ["target_field"],
            },
        }
    }

tools = [add_optional, 
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

# model = "gpt-3.5-turbo-1106"
model = "gpt-4-1106-preview"

#https://platform.openai.com/docs/guides/function-calling
def documentation_walkthrough(messages):
    print("Running on model", model)
    # Step 1: send the conversation and available functions to the model
    client = OpenAI(api_key="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")
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        temperature=0,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls 
    function_responses = []

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "addOptionalFunction": addOptionalFunction,
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