from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class SetDefaultSchema(BaseModel):
    source_field: str = Field(description="should be a a singular field name from the source record")
    target_field: str = Field(description="should be a singular field name from the target record corresponding to the source_field")
    default_value: str = Field(description="should be the default value of the given target schema's field")
    
class SetDefaultTool(BaseTool):
    name: str = "SET_DEFAULT_TOOL"
    description: str = "Tool that returns the mapping operator that sets the default value of a target schema's field"
    args_schema: Type[SetDefaultSchema] = SetDefaultSchema
    
    def _run(
        self,
        source_field: str,
        target_field: str,
        default_value: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TYPE {default_value} }}'   
    
    def _arun(
        self,
        source_field: str,
        target_field: str,
        default_value: str
    ) -> str:
        raise NotImplementedError
