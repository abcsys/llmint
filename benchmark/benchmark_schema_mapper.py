import os

import llmint.mapper.command.model as model
import llmint.mapper.command.util as util

__dir__ = os.path.dirname(__file__)
# load schema training examples
motion_sensor_dataset = os.path.join(
    __dir__, "..", "..", 
    "mint-sample-data",
    "schema", "motionsensors.yaml"
)
# load schema testing examples
motion_sensor_mappings = os.path.join(
    __dir__, "..", "..",
    "mint-sample-data",
    "schema", "motionsensors_mappings.yaml"
)

example_schemas = util.from_yaml(motion_sensor_dataset)
example_mappings = util.from_yaml(motion_sensor_mappings)
num_examples = len(example_schemas)
num_tests = len(example_mappings)

messages = []
util.get_system_prompt(messages)

def zero_shot_benchmark():
    all_precision = []
    all_recall = []
    all_f1 = []
    print("========== Zero Shot Benchmarking for motionsensors.yaml ==========", flush=True)
    for i in range(3):
        print(f"---------- Running Example {i} {str(example_schemas[i % num_examples]["name"])} to {str(example_schemas[(i + 1) % num_examples]["name"])} ----------", flush=True)
        zero_shot_messages = messages.copy()
        # user message
        zero_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = model.call(zero_shot_messages)
        precision, recall, f1 = util.accuracy(responses[0], i, example_mappings)
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)
        print(f"-------------------------------------------------------------", flush=True)
    for i in range(3):
        print(f"---------- Running Example {i + 3} {str(example_schemas[i]["name"])} to {str(example_schemas[i - 1]["name"])} ----------", flush=True)
        zero_shot_messages = messages.copy()
        # user message
        zero_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[i]), 
                                                                    str(example_schemas[i - 1]))
                                 })
        responses = model.call(zero_shot_messages)
        precision, recall, f1 = util.accuracy(responses[0], i + 3, example_mappings)
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)
        print(f"-------------------------------------------------------------", flush=True)
    print("=========================================================", flush=True)
    return all_precision, all_recall, all_f1

def multi_zero_shot_benchmark(num_runs):
    total_precision = [0] * 6
    total_recall = [0] * 6
    total_f1 = [0] * 6
    
    for i in range(num_runs):
        precision, recall, f1 = zero_shot_benchmark()
        total_precision = [a + b for a, b in zip(total_precision, precision)]
        total_recall = [a + b for a, b in zip(total_recall, recall)]
        total_f1 = [a + b for a, b in zip(total_f1, f1)]
        print(total_precision, total_recall, total_f1)
    
    print("Average Precision: ", [p / num_runs for p in total_precision], flush=True)
    print("Average Recall: ", [r / num_runs for r in total_recall], flush=True)
    print("Average F1: ", [f / num_runs for f in total_f1], flush=True)
        
    

"""
def one_shot_benchmark():
    print("========== One Shot Benchmarking for motionsensors.yaml ==========")
    for i in range(len(example_schemas)):
        print(f"---------- Running Example {i} ----------")
        print(f"Using example {example_mappings[(i + 1) % num_examples]["name"]}")
        one_shot_messages = messages.copy() 
        # first example
        one_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[(i + 1) % num_examples]), 
                                                                    str(example_schemas[(i + 2) % num_examples]))
                                 })
        one_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 1) % num_examples]["mapping"])
                                 })
        # user message
        one_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = model.call(one_shot_messages)
        print("Accuracy: ", util.accuracy(responses[0], i, example_mappings))
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
                                    "content": util.format_source_target(str(example_schemas[(i + 1) % num_examples]), 
                                                                    str(example_schemas[(i + 2) % num_examples]))
                                 })
        two_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 1) % num_examples]["mapping"])
                                 })
        # second example
        two_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[(i + 2) % num_examples]), 
                                                                    str(example_schemas[(i + 3) % num_examples]))
                                 })
        two_shot_messages.append({
                                    "role": "assistant",
                                    "content": str(example_mappings[(i + 2) % num_examples]["mapping"])
                                 })
        # user message
        two_shot_messages.append({
                                    "role": "user",
                                    "content": util.format_source_target(str(example_schemas[i % num_examples]), 
                                                                    str(example_schemas[(i + 1) % num_examples]))
                                 })
        responses = model.call(two_shot_messages)
        print("Accuracy: ", util.accuracy(responses[0], i, example_mappings))
        print(f"------------------------------")
    print("========================================")
"""

# zero_shot_benchmark()
multi_zero_shot_benchmark(20)