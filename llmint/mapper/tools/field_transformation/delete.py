from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class DeleteSchema(BaseModel):
    source_field: str = Field(description="should be a singular field name which is present in the source schema but not present in the target schema")
    
class DeleteTool(BaseTool):
    name: str = "DELETE_TOOL"
    description: str = "Tool that returns the mapping operator between a source and target schema field where the field is present in the source schema but not in the target schema"
    args_schema: Type[DeleteSchema] = DeleteSchema
    
    def _run(
        self,
        source_field: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {source_field}, to: , transformation: DELETE {source_field} }}'   
    
    def _arun(
        self,
        source_field: str
    ) -> str:
        raise NotImplementedError
