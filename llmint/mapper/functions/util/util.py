import yaml
import os
from termcolor import colored
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
                       sendMessageFunction)

class pcolors:
    RIGHT = '\033[92m'
    WRONG = '\033[91m'
    MISSING = '\033[33m'
    ENDC = '\033[0m'

# Read OpenAI key from ~/.llmint/config.yaml
def get_openai_api_key():
    with open(os.path.expanduser("~/.llmint/config.yaml"), "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        if "openai_api_key" not in config:
            raise Exception("OpenAI API key not found in ~/.llmint/config.yaml,"
                            " please add 'openai_api_key: YOUR_KEY' in the file.")
        openai_api_key = config["openai_api_key"]
        return openai_api_key

def from_yaml(filepath):
    """Load a YAML file and return the data."""
    with open(filepath, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)
    
def format_source_target(source, target):
    return "Source Schema: " + source + "\nTarget Schema: " + target

# accuracy measured by # of correct mappings / total mappings
def accuracy(results, example_num, example_mappings):
    correct = False
    correctIdxs = []
    numCorrect = 0
    total = 0
    print("Generated Mappings:", flush=True)
    for result, reasoning in results:
        for i in range(len(example_mappings[example_num]["mapping"])):
            if result == str(example_mappings[example_num]["mapping"][i]).replace("'", ""):
                print(pcolors.RIGHT + result + pcolors.ENDC + '\n', reasoning, flush=True)
                numCorrect += 1
                correctIdxs.append(i)
                correct = True 
        if not correct: 
            print(pcolors.WRONG + result + pcolors.ENDC + '\n', reasoning, flush=True)
        correct = False
        total += 1
    print("Ground Truth Mappings:", flush=True)
    for i in range(len(example_mappings[example_num]["mapping"])):
        if i in correctIdxs:
            print(pcolors.RIGHT + str(example_mappings[example_num]["mapping"][i]).replace("'", "") + pcolors.ENDC, flush=True)
        else:
            print(pcolors.MISSING + str(example_mappings[example_num]["mapping"][i]).replace("'", "") + pcolors.ENDC, flush=True)           
    print("Recall: ", len(correctIdxs), "/", len(example_mappings[example_num]["mapping"]), flush=True)
    print("Precision: ", len(correctIdxs), "/", len(results), flush=True)
    print("Total: ", numCorrect, "/", total, flush=True)
        
def print_responses(response, include_reasoning):
    for result, reasoning in response:
        if include_reasoning:
            print(pcolors.RIGHT + result + pcolors.ENDC + '\n', reasoning, flush=True)
        else:
            print(pcolors.RIGHT + result + pcolors.ENDC, flush=True)
    
        
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
        case "changeTypeFunction":
            return changeTypeFunction(source_field=args.get("source_field"),
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
        case "sendMessageFunction":
            return sendMessageFunction(message=args.get("message"))
                                     