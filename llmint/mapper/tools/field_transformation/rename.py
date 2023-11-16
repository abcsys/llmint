from langchain.chains import LLMMathChain
from langchain.utilities import SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool

from typing import Optional, Type
from pydantic import BaseModel, Field


class RenameToolSchema(BaseModel):
    source_field: str = Field(description="should be a singular field name from the source record")
    target_field: str = Field(description="should be a singular field name from the target record corresponding to the source_field")

class RenameTool(BaseTool):
    name: str = "RENAME_TOOL"
    description: str = "Tool that returns the mapping operator between a source and target schema field with different names"
    args_schema: Type[RenameToolSchema] = RenameToolSchema
    
    def _run(
        self,
        source_field: str, 
        target_field: str
    ) -> str:
        """Use the tool"""
        return f'{{ from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field} }}'   
    
    def _arun(
        self,
        source_field: str, 
        target_field: str
    ) -> str:
        raise NotImplementedError