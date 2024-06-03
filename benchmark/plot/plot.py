import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import llmint.mapper.command.api as api
import llmint.mapper.command.util as util

def append_to_csv(data_filename, csv_filename):
    # load data examples
    __dir__ = os.path.dirname(__file__)
    schemas = os.path.join(
        __dir__, "../..", "..",
        "mint-sample-data",
        "schema", data_filename
    )
    
    plot_schemas = util.from_yaml(schemas)
    
    data = []
    for i in range(len(plot_schemas) - 1):
        response_info = api.map(str(plot_schemas[i]), str(plot_schemas[i + 1]), include_info=True)
        data.append([len(response_info[0]), response_info[2], response_info[3]])
    
    with open(csv_filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
        
def plot(filename):
    __dir__ = os.path.dirname(__file__)
    csv_file = os.path.join(
        __dir__, "../..",
        filename
    )
    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.scatter(df['Num Mappings'], df['Response Latency'], label='Response Latency', marker='o')  # Line plot for response latency
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

plot("latency_v_mappings.csv")
        