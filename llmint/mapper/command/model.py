import json
from openai import OpenAI

import llmint.mapper.command.util as util

# ------------------------------------------------------------------------
# Field Transformation Tools
# ------------------------------------------------------------------------
def doNothingFunction(source_field, target_field, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: KEEP}}', reasoning)   

def addOptionalFunction(target_field, field_type, reasoning):
    return (f'{{from: None, to: {target_field}, transformation: ADD {target_field} TYPE {field_type}}}', reasoning)   

def castFunction(source_field, target_field, source_type, target_type, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: CAST {source_field} FROM {source_type} TO {target_type}}}', reasoning)

def deleteFunction(source_field, reasoning):
    return (f'{{from: {source_field}, to: None, transformation: DELETE {source_field}}}', reasoning)

def renameFunction(source_field, target_field, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field}}}', reasoning)

def setDefaultFunction(source_field, target_field, default_value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TO {default_value}}}', reasoning)

# ------------------------------------------------------------------------
# Value Transformation Tools
# ------------------------------------------------------------------------

def applyFuncFunction(source_field, target_field, function_name, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: APPLY_FUNC {source_field} {function_name}}}', reasoning) 

def mapFunction(source_field, target_field, old_value, new_value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: MAP {source_field} "{old_value}" TO "{new_value}"}}', reasoning)

def scaleFunction(source_field, target_field, factor, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SCALE {source_field} BY {factor}}}', reasoning)   

def shiftFunction(source_field, target_field, value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SHIFT {source_field} BY {value}}}', reasoning)   

# ------------------------------------------------------------------------
# Extended Command Tools
# ------------------------------------------------------------------------
def combineFunction(field_1, field_2, new_field, operation, reasoning):
     return (f'{{from: ({field_1}, {field_2}), to: {new_field}, transformation: COMBINE {field_1}, {field_2} TO {new_field} USING {operation}}}', reasoning)

def splitFunction(source_field, new_field_1, new_field_2, reasoning, delimiter=None):
    return (f'{{from: {source_field}, to: ({new_field_1}, {new_field_2}), transformation: SPLIT {source_field} INTO {new_field_1}, {new_field_2} BY {delimiter}}}', reasoning) 

def missingFunction(target_field, reasoning):
    return (f'{{from: None, to: {target_field}, transformation: MISSING {target_field}}}', reasoning)

def complexConversionFunction(source_field, target_field, conversion_equation, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: CONVERT {conversion_equation}}}', reasoning)

def sendMessageFunction(message):
    return (message, "No reasoning")

# ------------------------------------------------------------------------
# Function Router
# ------------------------------------------------------------------------
def call_fn(name, args):
    match name:
        case "doNothingFunction":
            return doNothingFunction(source_field=args.get("source_field"), 
                                     target_field=args.get("target_field"), 
                                     reasoning=args.get("reasoning"))
        case "addOptionalFunction":
            return addOptionalFunction(target_field=args.get("target_field"), 
                                       field_type=args.get("field_type"),
                                       reasoning=args.get("reasoning"))
        case "castFunction":
            return castFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      source_type=args.get("source_type"),
                                      target_type=args.get("target_type"),
                                      reasoning=args.get("reasoning"))
        case "deleteFunction":
            return deleteFunction(source_field=args.get("source_field"),
                                  reasoning=args.get("reasoning"))
        case "renameFunction":
            return renameFunction(source_field=args.get("source_field"),
                                  target_field=args.get("target_field"),
                                  reasoning=args.get("reasoning"))
        case "setDefaultFunction":
            return setDefaultFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      default_value=args.get("default_value"),
                                      reasoning=args.get("reasoning"))
        case "applyFuncFunction":
            return applyFuncFunction(source_field=args.get("source_field"), 
                                     target_field=args.get("target_field"), 
                                     function_name=args.get("function_name"),
                                     reasoning=args.get("reasoning"))
        case "mapFunction":
            return mapFunction(source_field=args.get("source_field"), 
                               target_field=args.get("target_field"), 
                               old_value=args.get("old_value"),
                               new_value=args.get("new_value"),
                               reasoning=args.get("reasoning"))
        case "scaleFunction":
            return scaleFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 factor=args.get("factor"),
                                 reasoning=args.get("reasoning"))
        case "shiftFunction":
            return shiftFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 value=args.get("value"),
                                 reasoning=args.get("reasoning"))
        case "combineFunction":
            return combineFunction(field_1=args.get("field_1"),
                                   field_2=args.get("field_2"),
                                   new_field=args.get("new_field"),
                                   operation=args.get("operation"),
                                   reasoning=args.get("reasoning"))
        case "splitFunction":
            return splitFunction(source_field=args.get("source_field"),
                                 new_field_1=args.get("new_field_1"),
                                 new_field_2=args.get("new_field_2"),
                                 delimiter=args.get("delimiter"),
                                 reasoning=args.get("reasoning"))
        case "missingFunction":
            return missingFunction(target_field=args.get("target_field"),
                                   reasoning=args.get("reasoning"))
        case "complexConversionFunction":
            return complexConversionFunction(source_field=args.get("source_field"),
                                             target_field=args.get("target_field"),
                                             conversion_equation=args.get("conversion_equation"),
                                             reasoning=args.get("reasoning"))
        case "sendMessageFunction":
            return sendMessageFunction(message=args.get("message"))
                                     

# ------------------------------------------------------------------------
# Function STL
# ------------------------------------------------------------------------
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

cast = {
    "type": "function",
    "function": {
        "name": "castFunction",
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

# ------------------------------------------------------------------------
# LLMint Model
# ------------------------------------------------------------------------

command = [
    doNothing,
    addOptional,
    cast,
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
    sendMessage
        ]

# model = "gpt-3.5-turbo-1106"
model = "gpt-4-1106-preview"

#https://platform.openai.com/docs/guides/function-calling
def call(messages):
    print("Running on model", model)
    # Step 1: send the conversation and available functions to the model
    client = OpenAI(api_key=util.get_openai_api_key())

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=command,
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
            "castFunction": castFunction,
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