import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

from field_transformation.functions import addFunction, changeTypeFunction, deleteFunction, renameFunction, setDefaultFunction

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
        case "addFunction":
            return addFunction(target_field=args.get("target_field"), 
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