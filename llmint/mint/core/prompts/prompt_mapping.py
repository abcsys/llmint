"""
Mint mapping schema.

TBD turn the following into the OpenAI function calling schema
FieldTransformation:
  - command: RENAME
    syntax: RENAME <field_name> TO <new_field_name>
    example: RENAME status TO light_status

  - command: CHANGE_TYPE
    syntax: CHANGE_TYPE <field_name> TO <new_type>
    example: CHANGE_TYPE brightness TO float

  - command: DELETE
    syntax: DELETE <field_name>
    example: DELETE light_color

  - command: ADD
    syntax: ADD <field_name> TYPE <type>
    example: ADD manufacturer TYPE string

  - command: SET_DEFAULT
    syntax: SET_DEFAULT <field_name> TO <default_value>
    example: SET_DEFAULT manufacturer TO Samsung

ValueTransformation:
  - command: MAP
    syntax: MAP <field_name> "<old_value>" TO "<new_value>"
    example: MAP status "on" TO "active"

  - command: SCALE
    syntax: SCALE <field_name> BY <factor>
    example: SCALE brightness BY 2

  - command: SHIFT
    syntax: SHIFT <field_name> BY <value>
    example: SHIFT brightness BY -5

  - command: APPLY_FUNC
    syntax: APPLY_FUNC <field_name> <FUNCTION_NAME>
    example: APPLY_FUNC light_color TO_UPPERCASE

ExtendedCommands:
  - command: SPLIT
    syntax: SPLIT <field_name> INTO <new_field_1>, <new_field_2> BY <delimiter>
    example: SPLIT name INTO first_name, last_name BY " "

  - command: COMBINE
    syntax: COMBINE <field_1>, <field_2> TO <new_field_name> USING <operation>
    example: COMBINE first_name, last_name TO full_name USING CONCATENATE
"""