from langchain.chains import LLMMathChain
from langchain.utilities import SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool

from typing import Optional, Type
from pydantic import BaseModel, Field


class RenameToolSchema(BaseModel):
    source_field: str = Field(description="should be a a singular field name from the source record")
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

llm = ChatOpenAI(temperature=0, 
                 openai_api_key="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")
tools = [RenameTool()]
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

print(agent.run("""
          
Generate the mapping operators required to translate from the source schema 
to the target schema. There may be multiple operators needed for a single field. 
          
Source Schema: Smart_light
- Kind: smart light
- Description: Sample source schema for a smart light

Fields:
- Name: power
  Type: Enum
  Range: ["on", "off"]

Target Schema: Smart_light
- Kind: smart light
- Description: Sample target schema for a smart light

Fields:
- Name: status
  Type: Enum
  Range: ["on", "off"]
          """))
