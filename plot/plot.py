import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import llmint.mapper.command.api as api
import llmint.mapper.command.util as util

def append_to_csv(data_filename, csv_filename, llmint = True):
    # load data examples
    __dir__ = os.path.dirname(__file__)
    schemas = os.path.join(
        __dir__, "..", "..", 
        "mint-sample-data",
        "schema", data_filename
    )
    
    plot_schemas = util.from_yaml(schemas)
    
    data = []
    for i in range(len(plot_schemas) - 1):
        print("Running test {}".format(i), flush=True)
        if llmint:
            # using llmint model 
            response_info = api.map(str(plot_schemas[i]), str(plot_schemas[i + 1]), include_info=True)
            data.append([response_info[1], response_info[2]])
        else:
            # using base model
            response_info = api.base_model_map(str(plot_schemas[i]), str(plot_schemas[i + 1]))
            data.append([response_info[1], response_info[2]])
    
    with open(csv_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
        
def plot(filename):
    __dir__ = os.path.dirname(__file__)
    csv_file = os.path.join(
        __dir__, "..",
        filename
    )
    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.scatter(df['Test'], df['Tokens'], label='Response Latency', marker='o')  # Line plot for response latency
    plt.scatter(df['Num Mappings'], df['Function Latency'], label='Function Latency', marker='x')  # Line plot for function latency
    
    # best fit lines
    plt.plot(np.unique(df['Num Mappings']), np.poly1d(np.polyfit(df['Num Mappings'], df['Response Latency'], 1))(np.unique(df['Num Mappings'])))
    plt.plot(np.unique(df['Num Mappings']), np.poly1d(np.polyfit(df['Num Mappings'], df['Function Latency'], 1))(np.unique(df['Num Mappings'])))

    plt.title('Num Mappings vs Latencies')
    plt.xlabel('Num Mappings')
    plt.ylabel('Latency (s)')
    plt.legend() 

    plt.grid(True)
    plt.show()
    
def plot_base_vs_llmint(base, llmint, column):
    __dir__ = os.path.dirname(__file__)
    base_data = os.path.join(
        __dir__, "..",
        base
    )
    
    llmint_data = os.path.join(
        __dir__, "..",
        llmint
    )
    base_df = pd.read_csv(base_data)
    llmint_df = pd.read_csv(llmint_data)
    
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.scatter(base_df['Test'], base_df[column], label='Base Model {}'.format(column), marker='o')  # Line plot for response latency
    plt.scatter(llmint_df['Test'], llmint_df[column], label='Llmint {}'.format(column), marker='x')  # Line plot for function latency
    
    plt.title('Test Case Num vs. {}'.format(column))
    plt.xlabel('Test Case Number')
    plt.ylabel(column)
    plt.legend() 

    plt.grid(True)
    plt.show()

#append_to_csv("motionsensorsv2.yaml", "base_tokens_latency.csv", llmint=False)
#append_to_csv("motionsensorsv2.yaml", "llmint_tokens_latency.csv", llmint=True)
plot_base_vs_llmint("base_tokens_latency.csv", "llmint_tokens_latency.csv", "Latency")
        