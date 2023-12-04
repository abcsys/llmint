import os
from function_model import *
from util.util import *

__dir__ = os.path.dirname(__file__)
# load schema training examples
motion_sensor_dataset = os.path.join(
    __dir__, "..", "..", "..", "..", 
    "mint-sample-data",
    "schema", "motionsensors.yaml"
)
# load schema testing examples
motion_sensor_mappings = os.path.join(
    __dir__, "..", "..", "..", "..",
    "mint-sample-data",
    "schema", "motion_sensors_mappings.yaml"
)
example_schemas = from_yaml(motion_sensor_dataset)
example_mappings = from_yaml(motion_sensor_mappings)
num_examples = len(example_schemas)

# very first instructional message sent to the model
messages = [{"role": "system",
             "content": """
                        Your job is to decide which of the provided functions are required to translate between a source and target schema.
                        You may pick as many mapping functions as you need to fully translate between the schemas, but try to use as few as possible. 
                        The most important part is picking the mapping functions, other comments are not required.
                        Do not make any assumptions about the schema. The only information you should use to guide your response is what is described in the schemas.
                        If you do not have enough information to completely translate between source fields and target fields, use the missing function.
                        If you are unsure whether or not two fields correspond to each other, assume that they do not correspond to each other.
                        Only consider two fields corresponding if you are absolutely confident based on the field descriptions.
                        """
            }]

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
        print("Accuracy: ", accuracy(responses, i, example_mappings))
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
        print("Accuracy: ", accuracy(responses, i, example_mappings))
        print(f"------------------------------")
    print("========================================")
    
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
        print("Accuracy: ", accuracy(responses, i, example_mappings))
        print(f"------------------------------")
    print("========================================")

zero_shot_benchmark()