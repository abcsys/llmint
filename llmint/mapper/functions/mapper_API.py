from function_model import *
from util.util import *


def mapper_API(source_schema, target_schema, include_reasoning=False):
    """ Return the mapping for a given source schema and target schema.
    
    source_schema: string representing the source schema
    target_schema: string representing the target schema
    include_reasoning: boolean indicating whether or not to print model's reasoning in the output
    """
    with open("instructions/llmint_base.txt") as f:
        messages = [{"role": "system",
                    "content": f.read()
                }]
    # STL instructional message sent to the model
    with open("instructions/stl_base.txt") as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })
    # end instructional message sent to the model
    with open("instructions/end_base.txt") as f:
        messages.append({"role": "system",
                        "content": f.read()
                        })  
    messages.append({
        "role": "user",
        "content": format_source_target(source_schema, target_schema)
    })
    
    response = documentation_walkthrough(messages)
    print_responses(response, include_reasoning)

source_schema = """
- name: "Neo Coolcam"
  kind: "motion sensor"
  description: "Attributes for the Neo Coolcam motion sensor system, known for its affordability and ease of integration with various smart home systems."
  fields:
    - name: "motion_detected"
      type: "boolean"
      description: "True if motion is detected, allowing for automation and security alerts."
      required: true

    - name: "lux"
      type: "integer"
      description: "Measures the light intensity in lux, useful for triggering lighting adjustments."
      required: false

    - name: "battery_level"
      type: "integer"
      description: "Current battery level percentage, indicating when a replacement is needed."
      required: false

    - name: "tamper_detection"
      type: "boolean"
      description: "Indicates if the sensor has been tampered with, enhancing security measures."
      required: false

    - name: "enabled"
      type: "boolean"
      description: "Indicates whether the motion sensor is enabled (True) or bypassed (False)."
      required: true
"""

target_schema = """
- name: "Aeotec Multisensor"
  kind: "motion sensor"
  description: "Attributes for the Aeotec Multisensor system, offering multiple sensing capabilities including motion, temperature, humidity, light, UV, and vibration."
  fields:
    - name: "motion_detected"
      type: "boolean"
      description: "True if motion is detected."
      required: true

    - name: "lux"
      type: "integer"
      description: "Light intensity measured in lux."
      required: false

    - name: "vibration"
      type: "boolean"
      description: "Indicates if vibration has been detected, useful for additional security monitoring."
      required: false

    - name: "enabled"
      type: "boolean"
      description: "Indicates whether the motion sensor is enabled (True) or bypassed (False)."
      required: true
"""

mapper_API(source_schema, target_schema, True)