from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class CombineSchema(BaseModel):
    field_1: str = Field(description="should be a source field name")
    field_2: str = Field(description="should be a source field name")
    new_field: str = Field(description="should be a singular target field name that is a combination of field_1 and field_2")
    operation: str = Field(description="should be the function to use for combining")
    
class CombineTool(BaseTool):
    name: str = "MAP_TOOL"
    description: str = "Tool that returns the mapping operator between a 2 source fields and 1 target fields where the target field is a combination of the source fields"
    args_schema: Type[CombineSchema] = CombineSchema
    
    def _run(
        self,
        field_1: str,
        field_2: str,
        new_field: str,
        operation: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: ({field_1} {field_2}), to: new_field, transformation: COMBINE {field_1}, {field_2} TO {new_field} USING {operation} }}'   
    
    def _arun(
        self,
        field_name: str,
        field_type: str
    ) -> str:
        raise NotImplementedError