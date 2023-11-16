from openai import OpenAI, ChatCompletion
from field_transformation.functions import addFunction, changeTypeFunction, deleteFunction, renameFunction, setDefaultFunction

from util.util import chat_completion_request, pretty_print_conversation, call_fn

import json

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

tools = [changeType, rename]

messages = [{"role": "system",
             "content": """
                        Generate the mapping operators required to translate from the source schema 
                        to the target schema. You may need to call multiple mapping tools in parallel to translate different
                        attributes of each field, ex. name and type.
                        """
            },
            {
             "role": "user",
             "content": """      
                        Source Schema: Smart_light
                        - Kind: smart light
                        - Description: Sample source schema for a smart light
                        
                        Source Fields:
                        - Name: power
                        Type: Enum
                        Range: ["on", "off"]

                        Target Schema: Smart_light
                        - Kind: smart light
                        - Description: Sample target schema for a smart light

                        Target Fields:
                        - Name: status
                        Type: int
                        Range: [1, 0]
                        """
            }]

# https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial
def tutorial():
    response = ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages,
        functions = tools,
        function_call = 'auto'
    )
    
    json_response = json.loads(response['choices'][0]['message']['function_call']['arguments'])
    return json_response

#https://platform.openai.com/docs/guides/function-calling
def documentation_walkthrough():
    # Step 1: send the conversation and available functions to the model
    client = OpenAI(api_key="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")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls 

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            #"addFunction": addFunction,
            "changeTypeFunction": changeTypeFunction,
            #"deleteFunction": deleteFunction,
            "renameFunction": renameFunction,
            #"setDefaultFunction": setDefaultFunction,
        }
        messages.append(response_message) # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name 
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = call_fn(function_name, function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            ) # extend conversation with function response
        
        print(messages)
        
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
    
def cookbook():
    chat_response = chat_completion_request(
        messages,
        tools=tools,
        tool_choice="auto",
    )
    assistant_message = chat_response.json()
    print(chat_response.json()['usage'])
    return assistant_message

print(documentation_walkthrough())