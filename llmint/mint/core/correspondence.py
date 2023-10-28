"""
Example:

name: "TemperatureMatch"
description: "Matching a single temperature field to a temperature field with units."
source: "SourceSchema"
target: "TargetSchema"
correspondences:
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
      - name: "unit"
        type: "string"
        description: "Unit of the temperature."
        required: true
        default: "fahrenheit"
"""

