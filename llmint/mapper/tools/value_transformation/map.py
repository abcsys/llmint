from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class MapSchema(BaseModel):
    field: str = Field(description="should be a a singular field name that has different values between the source and target schema")
    old_value: str = Field(description="should be the value of the field in the source schema")
    new_value: str = Field(description="should be the value of the field in the target schema")
    
class MapTool(BaseTool):
    name: str = "MAP_TOOL"
    description: str = "Tool that returns the mapping operator for a field who's value is of different types between the source and target schema"
    args_schema: Type[MapSchema] = MapSchema
    
    def _run(
        self,
        field: str,
        old_value: str,
        new_value: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {field} , to: {field}, transformation: MAP {field} "{old_value}" TO "{new_value}" }}'   
    
    def _arun(
        self,
        field_name: str,
        field_type: str
    ) -> str:
        raise NotImplementedError
