import yaml
from functions import (addOptionalFunction, 
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

def from_yaml(filepath):
    """Load a YAML file and return the data."""
    with open(filepath, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)
    
def format_source_target(source, target):
    return "Source Schema: " + source + "\nTarget Schema: " + target

# accuracy measured by # of correct mappings / total mappings
def accuracy(results, example_num, example_mappings):
    num_correct = 0
    for result in results:
        #print("========================================")
        for i in range(len(example_mappings[example_num]["mapping"])):
            #print("-------------------------------")
            #print(result)
            #print(str(example_mappings[example_num]["mapping"][i]).replace("'", ""))
            if result == str(example_mappings[example_num]["mapping"][i]).replace("'", ""):
                #print("match")
                num_correct += 1
            #print("-------------------------------")
        #print(("========================================"))
    return num_correct / len(example_mappings[example_num]["mapping"])

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
                                     