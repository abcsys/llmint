from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class ScaleSchema(BaseModel):
    field: str = Field(description="should be a a singular field name that has different values between the source and target schema")
    factor: str = Field(description="factor by which the field's value in the source schema should be scaled by to match the value in the target schema")
    
class ScaleTool(BaseTool):
    name: str = "SCALE_TOOL"
    description: str = "Tool that returns the mapping operator for a field who's value is of different scale between the source and target schema"
    args_schema: Type[ScaleSchema] = ScaleSchema
    
    def _run(
        self,
        field: str,
        factor: str,
    ) -> str:
        """Use the tool"""
        return f'{{ from: {field} , to: {field}, transformation: SCALE {field} BY {factor} }}'   
    
    def _arun(
        self,
        field: str,
        factor: str,
    ) -> str:
        raise NotImplementedError