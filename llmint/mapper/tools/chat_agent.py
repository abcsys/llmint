from langchain.agents import AgentType, initialize_agent, AgentExecutor, Tool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chains import LLMMathChain
from langchain.llms import OpenAI

from field_transformation.rename import RenameTool 
from field_transformation.add import AddTool
from field_transformation.change_type import ChangeTypeTool
from field_transformation.delete import DeleteTool
from field_transformation.set_default import SetDefaultTool

from value_transformation.apply_func import ApplyFuncTool
from value_transformation.map import MapTool
from value_transformation.scale import ScaleTool
from value_transformation.shift import ShiftTool

from extended_commands.combine import CombineTool 
from extended_commands.split import SplitTool

import pprint

llm = ChatOpenAI(temperature=0, 
                 model="gpt-3.5-turbo-0613",
                 openai_api_key="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")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
                    Generate the mapping operators required to translate from the source schema 
                    to the target schema. You may use multiple mapping tools to translate different
                    attributes of each field, ex. name and type.

                    Your final answer should only include the direct outputs of the tools you call.
                    This is what an example output should look like:

                    - <first tool raw output>
                    - <second tool raw output>
                    ...
                     
                  """
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [RenameTool(), 
         AddTool(), 
         ChangeTypeTool(), 
         DeleteTool(), 
         SetDefaultTool(),
         ApplyFuncTool(),
         MapTool(),
         ScaleTool(),
         ShiftTool(),
         CombineTool(),
         SplitTool()
        ]

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_functions(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

example = """
Source Schema: Smart_light
- Kind: smart light
- Description: Sample source schema for a smart light

Source Fields:
- Name: power
  Type: Enum
  Range: ["on", "off"]

Target Schema: Smart_light
- Kind: smart light
- Description: Sample target schema for a smart light

Target Fields:
- Name: status
  Type: int
  Range: [1, 0]
"""

trivial_example = "What is 5 times 2?"

pp = pprint.PrettyPrinter(width=41, compact=True)
"""
pp.pprint(agent_executor.invoke(
    {
        "input": example
    }
)['output'])
"""
agent_executor.run(example)