from langchain.tools import BaseTool

from typing import Optional, Type
from pydantic import BaseModel, Field

class ApplyFuncSchema(BaseModel):
    field_name: str = Field(description="should be a a singular field name that has different values between the source and target schema")
    function_name: str = Field(description="should be a function name which the  field's value in the source schema should be processed by to match the value in the target schema")
    
class ApplyFuncTool(BaseTool):
    name: str = "MAP_TOOL"
    description: str = "Tool that returns the mapping operator for a field who's target value is achieved by applying the function_name to the source value"
    args_schema: Type[ApplyFuncSchema] = ApplyFuncSchema
    
    def _run(
        self,
        field_name: str,
        function_name: str,
    ) -> str:
        """Use the tool"""
        return f'{{ from: {field_name} , to: {field_name}, transformation: APPLY_FUNC {field_name} {function_name} }}'   
    
    def _arun(
        self,
        field_name: str,
        field_type: str
    ) -> str:
        raise NotImplementedError