import llmint

def main():
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
    - name: "IKEA TRÅDFRI"
    kind: "light_bulb"
    description: "RGB color smart light bulb with adjustable brightness & color-temperature."
    fields:
        - name: "entity_id"
        type: "string"
        description: "Unique identifier for the TRÅDFRI device within Home Assistant."
        required: true
        
        - name: "power_state"
        - type: "boolean"
        - description: "True if the light is on, false if off."
        - required: true
        
        - name: "brightness"
        type: "integer"
        description: "Controls the brightness level of the light, from 0 (off) to 255 (maximum brightness)."
        required: false
        min: 0
        max: 255

        - name: "color_temp"
        type: "integer"
        description: "Sets the color temperature of the light in mireds, providing support for warm to cool white colors."
        required: false

        - name: "rgb_color"
        type: "list"
        description: "Defines the RGB color value for the light, allowing for a wide range of color settings."
        required: false

        - name: "transition"
        type: "integer"
        description: "Specifies the duration of the transition from the current state to the new state in seconds."
        required: false

        - name: "scene"
        type: "string"
        description: "Activates a predefined scene by name, adjusting multiple lighting devices to predefined settings."
        required: false
    """
    print(llmint.map(source_schema, target_schema))

if __name__ == "__main__":
    main()
