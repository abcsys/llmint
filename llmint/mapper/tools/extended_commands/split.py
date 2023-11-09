from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class SplitSchema(BaseModel):
    field_name: str = Field(description="should be a a singular field name that has different values between the source and target schema")
    new_field_1: str = Field(description="")
    new_field_2: str = Field(description="")
    delimiter: str = Field(description="")
    
class SplitTool(BaseTool):
    name: str = "MAP_TOOL"
    description: str = "Tool that returns the mapping operator for a field who's value is shifted between the source and target schema"
    args_schema: Type[SplitSchema] = SplitSchema
    
    def _run(
        self,
        field: str,
        value: str,
    ) -> str:
        """Use the tool"""
        return f'{{ from: {field} , to: {field}, transformation: SHIFT {field} BY {value} }}'   
    
    def _arun(
        self,
        field_name: str,
        field_type: str
    ) -> str:
        raise NotImplementedError