from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class ChangeTypeSchema(BaseModel):
    source_field: str = Field(description="should be a a singular field name from the source record")
    target_field: str = Field(description="should be a singular field name from the target record corresponding to the source_field")
    source_type: str = Field(description="should be the source type of the field name")
    target_type: str = Field(description="should be the target type of the field name")

class ChangeTypeTool(BaseTool):
    name: str = "CHANGE_TYPE_TOOL"
    description: str = "Tool that returns the mapping operator between a source and target schema field with different types"
    args_schema: Type[ChangeTypeSchema] = ChangeTypeSchema
    
    def _run(
        self,
        source_field: str,
        target_field: str, 
        source_type: str,
        target_type: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {source_field}, to: {target_field}, transformation: CHANGE TYPE {target_field} TO {target_type} }}'   
    
    def _arun(
        self,
        source_field: str,
        target_field: str, 
        source_type: str,
        target_type: str
    ) -> str:
        raise NotImplementedError
