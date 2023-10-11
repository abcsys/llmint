from typing import Dict


class Extract:
    def __init__(self, name="Unknown", description="Unknown schema"):
        self.name = name
        self.description = description

    @staticmethod
    def _get_type(value):
        if isinstance(value, str):
            return "string"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, bool):
            return "boolean"
        else:
            return "unknown"

    def extract_schema(self, data: Dict):
        """ Extracts schema from provided sample data. """
        fields = []

        for key, value in data.items():
            field = {
                "name": key,
                "type": self._get_type(value),
                "description": f"Description for {key}.",
                "required": True
            }

            # Setting some default values based on data type
            if field["type"] == "string":
                field["default"] = ""
            elif field["type"] == "integer":
                field["default"] = 0
                # Assuming brightness might have min-max, this is an example
                if key == "brightness":
                    field["min"] = 0
                    field["max"] = 100
            elif field["type"] == "float":
                field["default"] = 0.0

            fields.append(field)

        schema = {
            "name": self.name,
            "description": self.description,
            "fields": fields
        }

        return schema
