from test_functions import *

__dir__ = os.path.dirname(__file__)
motion_sensor_dataset = os.path.join(
    __dir__, "..", "..", "..", "..", 
    "mint-sample-data",
    "schema", "motionsensors.yaml"
)
motion_sensor_mappings = os.path.join(
    __dir__, "..", "..", "..", "..",
    "mint-sample-data",
    "schema", "motion_sensors_mappings.yaml"
)
example_schemas = from_yaml(motion_sensor_dataset)
example_mappings = from_yaml(motion_sensor_mappings)
num_examples = len(example_schemas)

def compare_results(results, example_num):
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

def simplisafe(num_shot, messages):
    if num_shot > 0:
        messages.append({
                         "role": "user",
                         "content": format_source_target(str(example_schemas[1]), 
                                                         str(example_schemas[2]))
                        })
        messages.append({
                         "role": "assistant",
                         "content": str(example_mappings[3]["mapping"])
                        })
    if num_shot > 1:
        messages.append({
                         "role": "user",
                         "content": format_source_target(str(example_schemas[2]), 
                                                         str(example_schemas[1]))
                        })
        messages.append({
                         "role": "assistant",
                         "content": str(example_mappings[5]["mapping"])
                        })
    for i in range(2):
        messages.append({
                        "role": "user",
                        "content": format_source_target(str(example_schemas[i]), 
                                                        str(example_schemas[(i + 1) % num_examples]))
                        })
    
messages = [{"role": "system",
             "content": """
                        Generate the mapping operators required to translate from the source schema 
                        to the target schema. Ensure that you translate all fields that differ between 
                        the source and target schema. The result by applying the mapping should be 
                        identitcal to the target schema. Only delete and add fields when there are
                        absolutely no other similar fields that can be renamed or change typed to. 
                        Make your mappings efficient. If a translation can be done with 1 mapping operation,
                        just use 1 mapping operation. You may use as many mapping tools as you need 
                        to translate different attributes of each field. For example, if a filed 
                        needs to be renamed and have its type changed to achieve the correct target
                        schema, you may call both the renameFunction and the changeTypeFunction on 
                        the same field.
                        """
            }]

def two_shot_benchmark():
    print("========== Two Shot Benchmarking for motionsensors.yaml ==========")
    for i in range(len(example_schemas)):
        print(f"---------- Running Example {i} ----------")
        print(f"Using example {example_mappings[(i + 1) % num_examples]["name"]} and {example_mappings[(i + 2) % num_examples]["name"]}")
        two_shot_messages = messages.copy()
        # first example
        two_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[(i + 1) % num_examples]), 
                                                                    str(example_schemas[(i + 2) % num_examples]))
                                 })
        two_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 1) % num_examples]["mapping"])
                                 })
        # second example
        two_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[(i + 2) % num_examples]), 
                                                                    str(example_schemas[(i + 3) % num_examples]))
                                 })
        two_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 2) % num_examples]["mapping"])
                                 })
        # user message
        two_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = documentation_walkthrough(two_shot_messages)
        print("Accuracy: ", compare_results(responses, i))
        print(f"------------------------------")
    print("========================================")

        
        

def one_shot_benchmark():
    print("========== One Shot Benchmarking for motionsensors.yaml ==========")
    for i in range(len(example_schemas)):
        print(f"---------- Running Example {i} ----------")
        print(f"Using example {example_mappings[(i + 1) % num_examples]["name"]}")
        one_shot_messages = messages.copy() 
        # first example
        one_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[(i + 1) % num_examples]), 
                                                                    str(example_schemas[(i + 2) % num_examples]))
                                 })
        one_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 1) % num_examples]["mapping"])
                                 })
        # user message
        one_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = documentation_walkthrough(one_shot_messages)
        print("Accuracy: ", compare_results(responses, i))
        print(f"------------------------------")
    print("========================================")
            

def zero_shot_benchmark():
    print("========== Zero Shot Benchmarking for motionsensors.yaml ==========")
    for i in range(len(example_schemas)):
        print(f"---------- Running Example {i} ----------")
        zero_shot_messages = messages.copy()
        # user message
        zero_shot_messages.append({
                                    "role": "user",
                                    "content": format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = documentation_walkthrough(zero_shot_messages)
        print("Accuracy: ", compare_results(responses, i))
        print(f"------------------------------")
    print("========================================")

zero_shot_benchmark()
one_shot_benchmark()
two_shot_benchmark()