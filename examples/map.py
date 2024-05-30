import llmint
import pprint as pp


"""
    Run python -m  examples.map from root llmint directory
"""


def main():
    mappings: list = llmint.map(source_schema, target_schema)
    pp.pprint(mappings)


source_schema = """
- name: "Vivint"
  kind: "motion sensor"
  description: "Attributes for the Vivint motion sensor system."
  fields:
    - name: "triggered"
      type: "boolean"
      description: "Indicates whether the sensor has been triggered."
      required: true

    - name: "enabled"
      type: "boolean"
      description: "Indicates whether the motion sensor is enabled (True) or bypassed (False)."
      required: true

    - name: "battery_level_percentage"
      type: "integer"
      description: "Measures the current battery level of the motion sensor."
      required: true
"""

target_schema = """
- name: "SimpliSafe"
  kind: "motion sensor"
  description: "Attributes for the SimpliSafe motion sensor system."
  fields:
    - name: "trigger_instantly"
      type: "boolean"
      description: "Indicates whether the sensor will trigger instantly."
      required: true

    - name: "triggered"
      type: "boolean"
      description: "Indicates whether the sensor has been triggered."
      required: true

    - name: "low_battery"
      type: "boolean"
      description: "Indicates whether the sensor's battery is low."
      required: true
"""

if __name__ == "__main__":
    main()
