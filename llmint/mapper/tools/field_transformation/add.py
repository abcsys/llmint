from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class AddSchema(BaseModel):
    target_field: str = Field(description="should be a a singular field name which is not present in the source schema but is present in the target schema")
    field_type: str = Field(description="should be the type of the field to be added")
    
class AddTool(BaseTool):
    name: str = "ADD_TOOL"
    description: str = "Tool that returns the mapping operator between a source and target schema field where the field is not present in the source schema but is present in the target schema"
    args_schema: Type[AddSchema] = AddSchema
    
    def _run(
        self,
        target_field: str,
        field_type: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: , to: {target_field}, transformation: ADD {target_field} TYPE {field_type} }}'   
    
    def _arun(
        self,
        field_name: str,
        field_type: str
    ) -> str:
        raise NotImplementedError
