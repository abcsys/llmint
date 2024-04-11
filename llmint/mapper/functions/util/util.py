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
                       complexConversionFunction,
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