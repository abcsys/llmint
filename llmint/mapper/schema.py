from llmint.mapper import Mapper
from langchain.chat_models import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from llmint import mint_utils
from llmint.mapper import Mapper
from llmint.mapper.output import format_output


class CorrespondenceMapper(Mapper):
    pass


class FieldMapper(Mapper):

    def format_input(self, source_schema, target_schema) -> dict:
        pass

    def invoke(self, source_schema, target_schema):
        """
        Decides whether to invoke the LLM based mapper or normal range mappers.

        """
        super().invoke(source_schema, target_schema)
