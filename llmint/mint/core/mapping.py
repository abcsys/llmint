"""
name: "TemperatureMapping"
description: "Mapping a temperature field in Celsius to Fahrenheit with unit."
source: "SourceSchema"
target: "TargetSchema"
mappings:
  - source:
      - name: "temp"
        type: "float"
        description: "Temperature in Celsius."
        required: true
        default: 0
    target:
      - name: "temperature"
        type: "float"
        description: "Temperature in Fahrenheit."
        required: true
        default: 32
        transformation:
          type: "linear"
          parameters:
            slope: 1.8
            intercept: 32
      - name: "unit"
        type: "string"
        description: "Unit of the temperature."
        required: true
        default: "fahrenheit"
        transformation:
          type: "constant"
          value: "fahrenheit"
"""