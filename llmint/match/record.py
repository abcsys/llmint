"""
Simple zero to few-shot matching.
"""

import time
from abc import ABC
from abc import abstractmethod
from langchain.chat_models import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from llmint import mint_utils


class RecordMatch(ABC):
    def __init__(
            self,
            examples=None,
            model="gpt-3.5-turbo",
            temperature=0.0,
            verbose=False,
    ):
        self.examples = examples or []
        self.model = model
        self.temperature = temperature
        self.verbose = verbose

        self.chain, self.prompt = self.prepare()
        self.token_counts = []
        self.latencies = []

    @abstractmethod
    def prepare(self) -> (LLMChain, str):
        """
        Prepares the prompt and LLMChain.
        """
        pass

    @abstractmethod
    def format_input(self, source_schema, target_schema) -> dict:
        pass

    def invoke(self, source_schema, target_schema):
        """
        Invokes the LLMChain for schema matching.

        Args:
        - source: The source schema.
        - target: The target schema.

        Returns:
        Correspondences between the source and target.
        """
        input = self.format_input(source_schema, target_schema)

        with get_openai_callback() as cb:
            start = time.time()
            output_message = self.chain.invoke(input)
            self.token_counts.append(cb.total_tokens)
            self.latencies.append(time.time() - start)
        return output_message


class RecordChatMatch(RecordMatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self):
        """
        Prepares the prompt and LLMChain.
        """
        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "The source schema is {source} and the target schema is {target}"),
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
                openai_api_key=mint_utils.get_openai_key(),
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
                  f"Answer using the same format as the example."
        return {"input_message": message}
