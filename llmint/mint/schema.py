"""
Llmint internal schema definition.

The Schema module provides a structure for defining and extracting the schema
from generic records. The module consists of various field classes, each
representing a specific datatype (e.g., String, Integer, Float, Enum, Boolean,
Array). Each field class can hold various properties such as name, type,
description, default value, example, and any other relevant constraints
(like min, max for numerical fields).

The main `Schema` class encapsulates the entire schema definition for a
specific type of record. It contains methods to automatically extract a
schema from a provided record. The schema extraction supports nested records
and various data types, providing a flexible and versatile framework for
schema representation.

Use Cases:
- Extract schema definitions from given records/data.
- Represent and define the structure of records for various domains.

Example:

Given a sample record for a smart light:
{
    "switch": ["on", "off"],
    "glow": 70,
    "shade": "green",
    "light_mode": "evening",
    "brightness_factor": 1.5,
    "config": {
        "auto_mode": True,
        "timer": {"start": "8:00", "end": "18:00"}
    }
}

After extracting its schema using the Schema class, you might get a representation like:

Schema: Smart_light
- Kind: smart light
- Description: Sample schema for a smart light

Fields:
- Name: switch
  Type: Enum
  Range: ["on", "off"]

- Name: glow
  Type: Integer
  Min: None
  Max: None

- Name: shade
  Type: String

- Name: light_mode
  Type: String

- Name: brightness_factor
  Type: Float
  Min: None
  Max: None

- Name: config
  Type: Object
  Subfields:
    - Name: auto_mode
      Type: Boolean

    - Name: timer
      Type: Object
      Subfields:
        - Name: start
          Type: String

        - Name: end
          Type: String
"""

import yaml
from typing import Any, List, Union, Optional, Dict


# Base Field definition class
class Field:
    """Base Field class."""

    def __init__(self,
                 name: str,
                 type_: str,
                 description: Optional[str] = None,
                 required: Optional[bool] = False,
                 default: Optional[Any] = None,
                 example: Optional[Any] = None,
                 subfields: Optional[List['Field']] = None):
        """Constructor for Field class."""
        self.name = name
        self.type_ = type_
        self.description = description
        self.required = required
        self.default = default
        self.example = example
        self.subfields = subfields


# Specific Field Types

class StringField(Field):
    """Represents a String field."""

    def __init__(self, name: str, **kwargs):
        super().__init__(name, "string", **kwargs)


class IntegerField(Field):
    """Represents an Integer field with optional min and max constraints."""

    def __init__(self, name: str, min_: Optional[int] = None, max_: Optional[int] = None, **kwargs):
        super().__init__(name, "integer", **kwargs)
        self.min_ = min_
        self.max_ = max_


class FloatField(Field):
    """Represents a Float field with optional min and max constraints."""

    def __init__(self, name: str, min_: Optional[float] = None, max_: Optional[float] = None, **kwargs):
        super().__init__(name, "float", **kwargs)
        self.min_ = min_
        self.max_ = max_


class EnumField(Field):
    """Represents an Enum field with a set range of values."""

    def __init__(self, name: str, range_: List[str], **kwargs):
        super().__init__(name, "enum", **kwargs)
        assert isinstance(range_, list), "Range for EnumField should be a list."
        self.range_ = range_


class BooleanField(Field):
    """Represents a Boolean field."""

    def __init__(self, name: str, **kwargs):
        super().__init__(name, "boolean", **kwargs)


class ArrayField(Field):
    """Represents an Array field with elements of a specified type."""

    def __init__(self, name: str, element_type: str, **kwargs):
        super().__init__(name, "array", **kwargs)
        self.element_type = element_type


# Main schema class
class Schema:
    """Represents a schema for a specific kind of record."""

    def __init__(self,
                 name: str,
                 kind: str,
                 description: str,
                 fields: List[Field]):
        """Constructor for Schema class."""
        self.name = name
        self.kind = kind
        self.description = description
        self.fields = fields

    @staticmethod
    def extract(record: Dict[str, Any], kind: str, description: str) -> 'Schema':
        """Extracts a schema based on the given record."""
        fields = Schema._recursive_extract(record)
        schema_name = kind.replace(" ", "_").capitalize()
        return Schema(name=schema_name, kind=kind, description=description, fields=fields)

    @staticmethod
    def _recursive_extract(record: Dict[str, Any]) -> List[Field]:
        """Recursively extracts fields from a given record."""
        fields = []
        for key, value in record.items():
            field_type = type(value).__name__

            # Determine field type and instantiate appropriate Field class
            if field_type == "str":
                fields.append(StringField(name=key))
            elif field_type == "int":
                fields.append(IntegerField(name=key))
            elif field_type == "float":
                fields.append(FloatField(name=key))
            elif field_type == "bool":
                fields.append(BooleanField(name=key))
            elif field_type == "list":
                # Consider first element type for array elements
                element_type = type(value[0]).__name__ if value else "NoneType"
                fields.append(ArrayField(name=key, element_type=element_type))
            elif field_type == "dict":
                # Handle nested records
                nested_fields = Schema._recursive_extract(value)
                fields.append(Field(name=key, type_="object", subfields=nested_fields))

        return fields

    def to_yaml(self) -> str:
        """Converts the schema to its YAML representation."""

        def field_to_dict(field: Field) -> dict:
            """Convert a field to its dictionary representation."""
            result = {}
            result['name'] = field.name
            result['type'] = field.type_

            # Conditional additions:
            if field.description:
                result['description'] = field.description
            if field.required:
                result['required'] = field.required
            if field.example:
                result['example'] = field.example

            if isinstance(field, EnumField):
                result['range'] = field.range_

            if isinstance(field, ArrayField):
                result['element_type'] = field.element_type

            if field.subfields:
                result['subfields'] = [field_to_dict(subfield) for subfield in field.subfields]

            # Place min and max at the end
            if isinstance(field, IntegerField) or isinstance(field, FloatField):
                if hasattr(field, 'min_'):
                    result['min'] = field.min_
                if hasattr(field, 'max_'):
                    result['max'] = field.max_

            return result

        # Ensure 'name' and 'kind' are placed at the beginning of the schema dictionary
        schema_dict = {
            'name': self.name,
            'kind': self.kind
        }
        if self.description:
            schema_dict['description'] = self.description
        schema_dict['fields'] = [field_to_dict(field) for field in self.fields]

        return yaml.dump(schema_dict, sort_keys=False)  # Keep insertion order


def test():
    import pprint as pp
    # Test
    record = {
        "switch": ["on", "off"],
        "glow": 70,
        "shade": "green",
        "light_mode": "evening",
        "brightness_factor": 1.5,
        "config": {
            "auto_mode": True,
            "timer": {"start": "8:00", "end": "18:00"}
        },
        "colors": ["red", "blue", "green"],
        "is_active": True
    }

    print(f"Input: {pp.pformat(record)}")
    parsed_schema = Schema.extract(record, kind="smart light", description="Sample schema")
    print(parsed_schema.name)  # Outputs: Smart_light
    print(parsed_schema.fields[5].type_)  # Outputs: object
    print(parsed_schema.fields[6].type_)  # Outputs: array
    print(parsed_schema.fields[6].element_type)  # Outputs: str
    print(parsed_schema.fields[7].type_)  # Outputs: boolean

    print("Output:")
    print(parsed_schema.to_yaml())


if __name__ == '__main__':
    test()
