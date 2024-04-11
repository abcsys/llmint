import json
from openai import OpenAI
from util.util import *
<<<<<<< HEAD
from functions import (doNothingFunction,
                       addOptionalFunction, 
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
                       missingFunction,
                       complexConversionFunction,
                       sendMessageFunction)
=======
from functions import (
    doNothingFunction,
    addOptionalFunction,
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
    missingFunction,
    sendMessageFunction
)
>>>>>>> 9e1c1aa665390971ef0dceb17c439c1076503db9

doNothing = {
    "type": "function",
    "function": {
        "name": "doNothingFunction",
        "description": "No transformation is needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field in the source schema",
                },
                "target_field": {
                    "type": "string",
                    "description": "Field in the target schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "field_type", "reasoning"],
        },
    }
}

addOptional = {
    "type": "function",
    "function": {
        "name": "addOptionalFunction",
        "description": "Add an optional target field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "field_type", "reasoning"],
        },
    }
}

changeType = {
    "type": "function",
    "function": {
        "name": "changeTypeFunction",
        "description": "Change the type of the source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "source_type", "target_type", "reasoning"],
        },
    }
}

delete = {
    "type": "function",
    "function": {
        "name": "deleteFunction",
        "description": "Delete a source field",
        "parameters": {
            "type": "object",
            "properties": {
                "source_field": {
                    "type": "string",
                    "description": "Field from the source schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "reasoning"],
        },
    }
}

rename = {
    "type": "function",
    "function": {
        "name": "renameFunction",
        "description": "Rename a source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "reasoning"],
        },
    }
}

set_default = {
    "type": "function",
    "function": {
        "name": "setDefaultFunction",
        "description": "Set the default of a target field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "default_value", "reasoning"],
        },
    }
}

apply_func = {
    "type": "function",
    "function": {
        "name": "applyFuncFunction",
        "description": "Apply a function to the values of a source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "function_name", "reasoning"],
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "old_value", "new_value", "reasoning"],
        },
    }
}

scale = {
    "type": "function",
    "function": {
        "name": "scaleFunction",
        "description": "Scale the value of a source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "factor", "reasoning"],
        },
    }
}

shift = {
    "type": "function",
    "function": {
        "name": "shiftFunction",
        "description": "Shift the value of a source field",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "target_field", "value", "reasoning"],
        },
    }
}

combine = {
    "type": "function",
    "function": {
        "name": "combineFunction",
        "description": "Combine 2 source fields",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["field_1", "field_2", "new_field", "operation", "reasoning"],
        },
    }
}

split = {
    "type": "function",
    "function": {
        "name": "splitFunction",
        "description": "Split the source field into 2 separate fields",
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
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["source_field", "new_field_1", "new_field_2", "reasoning"],
        },
    }
}

missing = {
    "type": "function",
    "function": {
        "name": "missingFunction",
        "description": "Indicates that the required target field is impossible to construct from the fields in the source schema",
        "parameters": {
            "type": "object",
            "properties": {
                "target_field": {
                    "type": "string",
                    "description": "Field from the target schema",
                },
                "reasoning": {
                    "type": "string",
                    "description": "In-depth reasoning as to why you chose this function",
                },
            },
            "required": ["target_field", "reasoning"],
        },
    }
}

complexConversion = {
        "type": "function",
        "function": {
            "name": "complexConversionFunction",
            "description": "Describes the equation needed to convert from source to target values",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "target_field": {
                        "type": "string",
                        "description": "Field from the target schema",
                    },
                    "conversion_equation": {
                        "type": "string",
                        "description": "Mathematical equation used in conversion. Let x be the source value and y be the target value.",
                    },
                    "reasoning": {
                        "type": "string", 
                        "description": "In-depth reasoning as to why you chose this function",
                    },
                },
                "required": ["source_field", "target_field", "conversion_equation", "reasoning"],
            },
        }
    }

sendMessage = {
    "type": "function",
    "function": {
        "name": "sendMessageFunction",
        "description": "Sends a message visible to the user",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to send to the user",
                },
            },
            "required": ["message"],
        },
    }
}

tools = [doNothing,
         addOptional,
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
         missing,
         complexConversion,
         sendMessage]

# model = "gpt-3.5-turbo-1106"
model = "gpt-4-1106-preview"

#https://platform.openai.com/docs/guides/function-calling
def function_model(messages):
    print("Running on model", model)
    # Step 1: send the conversation and available functions to the model
    client = OpenAI(api_key=get_openai_api_key())

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
            "doNothingFunction": doNothingFunction,
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
            "complexConversionFunction": complexConversionFunction,
            "sendMessageFunction": sendMessageFunction,
        }
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        print("LLMint calls", len(tool_calls), "functions")
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = call_fn(function_name, function_args)
            function_responses.append(function_response)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        # return function_responses
        print("Token Usage: ", response.usage)
    return function_responses
