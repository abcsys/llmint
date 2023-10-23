"""
Simple zero to few-shot mapping.
"""

from langchain.chat_models import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from llmint import mint_utils
from llmint.mapper import Mapper
import llmint.mapper.output as output_util
from llmint.mint.llm import LLM as MintLLM


class RecordChatMapper(Mapper, MintLLM):
    def __init__(self, *args, **kwargs):
        Mapper.__init__(self)
        MintLLM.__init__(self, *args, **kwargs)

    def prepare(self):
        """
        Prepares the prompt and LLMChain.
        """
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "The source schema is {source} and the target schema is {target}"),
                ("ai", "{mapping}")
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.examples
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are performing schema mapping to identify the "
                           "correspondences of fields and their transformations between "
                           "a source and a target schemas."),
                few_shot_prompt,
                ("human", "{input_message}")
            ]
        )

        chain = LLMChain(
            llm=ChatOpenAI(
                openai_api_key=mint_utils.get_openai_api_key(),
                temperature=self.temperature,
            ),
            prompt=prompt,
            output_parser=mint_utils.CommaSeparatedListOutputParser(),
            verbose=self.verbose,
        )

        return chain, prompt

    def format_input(self, source_schema, target_schema):
        message = f"What are the schema mappings " \
                  f"between schema {source_schema} " \
                  f"and schema {target_schema}? " \
                  f"Answer using the same format as the example."
        return {"input_message": message}

    def format_output(self, output):
        return output_util.format_output(output)

    def invoke(self, source_record, target_record):
        return MintLLM.invoke(self, source_record, target_record)
