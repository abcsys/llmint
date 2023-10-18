"""
Simple zero to few-shot matching.
"""

import time
from abc import ABC
from abc import abstractmethod
from langchain.chat_models import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from llmint import mint_utils
from llmint.match.util import format_output
from langchain.callbacks import get_openai_callback



class RecordMatch(Match):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RecordChatMatch(RecordMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self):
        """
        Prepares the prompt and LLMChain.
        """
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "The source schema is {source} and the target schema is {target}."),
                ("ai", "{correspondence}")
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.examples
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are performing schema matching to identify the "
                           "correspondences between a source and a target schemas."),
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
        message = f"What are the correspondences " \
                  f"between schema {source_schema} " \
                  f"and schema {target_schema}? " \
                  f"Answer using the same format as the example. "
        return {"input_message": message}
    
    def format_output(self, output):
        return format_output(output)