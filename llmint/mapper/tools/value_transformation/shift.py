from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class ShiftSchema(BaseModel):
    field: str = Field(description="should be a singular field name that has different values between the source and target schema")
    value: str = Field(description="value by which the field's value in the source schema should be shifted by to match the value in the target schema")
    
class ShiftTool(BaseTool):
    name: str = "SHIFT_TOOL"
    description: str = "Tool that returns the mapping operator for a field who's value is shifted between the source and target schema"
    args_schema: Type[ShiftSchema] = ShiftSchema
    
    def _run(
        self,
        field: str,
        value: str,
    ) -> str:
        """Use the tool"""
        return f'{{ from: {field} , to: {field}, transformation: SHIFT {field} BY {value} }}'   
    
    def _arun(
        self,
        field: str,
        value: str,
    ) -> str:
        raise NotImplementedError