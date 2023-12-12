from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class SplitSchema(BaseModel):
    source_field: str = Field(description="should be a a singular field name from the source schema")
    new_field_1: str = Field(description="should be a new target field name split from the source field name")
    new_field_2: str = Field(description="should be a new target field name split from the source field name")
    delimiter: str = Field(description="should be the delimiter character to split the source field name on")
    
class SplitTool(BaseTool):
    name: str = "SPLIT_TOOL"
    description: str = "Tool that returns the mapping operator between a source and target schema fields where the target fields are split from the source field"
    args_schema: Type[SplitSchema] = SplitSchema
    
    def _run(
        self,
        source_field: str,
        new_field_1: str,
        new_field_2: str,
        delimiter: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {source_field} , to: ({new_field_1} {new_field_2}), transformation: SPLIT {source_field} INTO {new_field_1}, {new_field_2} BY {delimiter} }}'   
    
    def _arun(
        self,
        source_field: str,
        new_field_1: str,
        new_field_2: str,
        delimiter: str
    ) -> str:
        raise NotImplementedError