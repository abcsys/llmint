import llmint
import pprint as pp


"""
    Run python -m  examples.map from root llmint directory
"""


def main():
    mappings: list = llmint.map(source_schema, target_schema)
    pp.pprint(mappings)


source_schema = """
- name: "Philips Hue Color Bulb"
  kind: "light_bulb"
  description: "RGB color smart light bulb with adjustable brightness."
  fields:
  - name: "color"
    type: "string"
    description: "Hexadecimal color value for the bulb."
    required: false

  - name: "brightness"
    type: "integer"
    description: "Brightness level from 0 to 100."
    required: true

  - name: "power_state"
    type: "boolean"
    description: "True if the light is on, false if off."
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
