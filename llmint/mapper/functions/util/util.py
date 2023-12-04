import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

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

GPT_MODEL = "gpt-3.5-turbo-0613"
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "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",
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "tool":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

def call_fn(name, args):
    match name:
        case "addOptionalFunction":
            return addOptionalFunction(target_field=args.get("target_field"), 
                               field_type=args.get("field_type"))
        case "changeTypeFunction":
            return changeTypeFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      source_type=args.get("source_type"),
                                      target_type=args.get("target_type"))
        case "deleteFunction":
            return deleteFunction(source_field=args.get("source_field"))
        case "renameFunction":
            return renameFunction(source_field=args.get("source_field"),
                                  target_field=args.get("target_field"))
        case "setDefaultFunction":
            return setDefaultFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      default_value=args.get("default_value"))
        case "applyFuncFunction":
            return applyFuncFunction(source_field=args.get("source_field"), 
                                     target_field=args.get("target_field"), 
                                     function_name=args.get("function_name"))
        case "mapFunction":
            return mapFunction(source_field=args.get("source_field"), 
                               target_field=args.get("target_field"), 
                               old_value=args.get("old_value"),
                               new_value=args.get("new_value"))
        case "scaleFunction":
            return scaleFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 factor=args.get("factor"))
        case "shiftFunction":
            return shiftFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 value=args.get("value"))
        case "combineFunction":
            return combineFunction(field_1=args.get("field_1"),
                                   field_2=args.get("field_2"),
                                   new_field=args.get("new_field"),
                                   operation=args.get("operation"))
        case "splitFunction":
            return splitFunction(source_field=args.get("source_field"),
                                 new_field_1=args.get("new_field_1"),
                                 new_field_2=args.get("new_field_2"),
                                 delimiter=args.get("delimiter"))
        case "missingFunction":
            return missingFunction(target_field=args.get("target_field"))
                                     