import os

from llmint.core import model, eval
from llmint.map import prompt
from benchmark import util

TRAINING_FILENAME = "motionsensors.yaml"
TESTING_FILENAME = "motionsensors_mappings.yaml"

__dir__ = os.path.dirname(__file__)

# load schema training examples
training = os.path.join(
    __dir__, "..", "..", 
    "mint-sample-data",
    "schema", TRAINING_FILENAME
)

# load schema testing examples
testing = os.path.join(
    __dir__, "..", "..",
    "mint-sample-data",
    "schema", TESTING_FILENAME
)

training_schemas = util.from_yaml(training)
testing_mappings = util.from_yaml(testing)
num_training_schemas = len(training_schemas)
num_test_mappings = len(testing_mappings)

messages = []
messages.append(prompt.system)

def zero_shot_benchmark():
    """Given a set of training schemas and the corresponding test mappings, print a log of accuracy metrics."""
    
    all_precision = []
    all_recall = []
    all_f1 = []
    
    print(f"========== Zero Shot Benchmarking for {TRAINING_FILENAME} ==========", flush=True)
    
    # pair training schemas (i, i+1), from i = [0, num_training_schemas - 1]
    for i in range(num_training_schemas):
        print(f"---------- Running Example {i} {str(training_schemas[i % num_training_schemas]["name"])} to {str(training_schemas[(i + 1) % num_training_schemas]["name"])} ----------", flush=True)
        source_schema = str(training_schemas[i])
        target_schema = str(training_schemas[(i + 1) % num_training_schemas])
        
        # query chatGPT
        responses = model.llmint.map(source_schema, target_schema)
        print(responses)
        
        # calculate accuracy metrics
        precision, recall, f1 = eval.accuracy(responses, testing_mappings[i]["mapping"])
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)
        print(f"-------------------------------------------------------------", flush=True)
        
    # pair training schemas (i, i-1), from i = [num_training schemas, 1]
    for i in range(num_training_schemas):
        print(f"---------- Running Example {i + 3} {str(training_schemas[i]["name"])} to {str(training_schemas[(i + num_training_schemas - 1) % num_training_schemas]["name"])} ----------", flush=True)
        source_schema = str(training_schemas[i])
        target_schema = str(training_schemas[(i + num_training_schemas - 1) % num_training_schemas])
    
        
        # query chatGPT
        responses = model.llmint.map(source_schema, target_schema)
        print(responses)
        
        # calculate accuracy metrics
        precision, recall, f1 = eval.accuracy(responses, testing_mappings[i + 3]["mapping"])
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)
        print(f"-------------------------------------------------------------", flush=True)
    print("=========================================================", flush=True)
    return all_precision, all_recall, all_f1

def multi_zero_shot_benchmark(num_runs):
    total_precision = [0] * num_test_mappings
    total_recall = [0] * num_test_mappings
    total_f1 = [0] * num_test_mappings
    
    for i in range(num_runs):
        precision, recall, f1 = zero_shot_benchmark()
        
        total_precision = [a + b for a, b in zip(total_precision, precision)]
        total_recall = [a + b for a, b in zip(total_recall, recall)]
        total_f1 = [a + b for a, b in zip(total_f1, f1)]
        print(total_precision, total_recall, total_f1)
    
    print("Average Precision: ", [p / num_runs for p in total_precision], flush=True)
    print("Average Recall: ", [r / num_runs for r in total_recall], flush=True)
    print("Average F1: ", [f / num_runs for f in total_f1], flush=True)

zero_shot_benchmark()
# multi_zero_shot_benchmark(20)