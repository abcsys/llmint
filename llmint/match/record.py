"""
Simple zero to few-shot matching.
"""

import time
from langchain.chat_models import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from llmint import mint_utils


class SimpleMatch:
    def __init__(self, examples=None, temperature=0.0):
        self.examples = examples or []
        self.temperature = temperature
        self.chain, self.prompt = self.prepare()
        self.token_counts = []
        self.latencies = []

    def prepare(self):
        """
        Prepares the ChatPrompt and LLMChain.
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
                           "correspondences of fields between a source and a target schemas."),
                few_shot_prompt,
                ("human", "{input_message}")
            ]
        )

        chain = LLMChain(
            llm=ChatOpenAI(
                openai_api_key=mint_utils.get_openai_key(),
                temperature=self.temperature
            ),
            prompt=prompt,
            output_parser=mint_utils.CommaSeparatedListOutputParser()
        )

        return chain, prompt

    def invoke(self, source_schema, target_schema, dry_run=False):
        """
        Invokes the LLMChain for schema matching.

        Args:
        - source: The source schema.
        - target: The target schema.
        - dry_run: If true, returns the formatted prompt without making an actual API call.

        Returns:
        Correspondences between the source and target.
        """
        input_message = f"What are the correspondences " \
                        f"between {source_schema} and {target_schema}?"

        if dry_run:
            return self.prompt.format(input_message=input_message)
        with get_openai_callback() as cb:
            start = time.time()
            output_message = self.chain.invoke({"input_message": input_message})
            self.token_counts.append(cb.total_tokens)
            self.latencies.append(time.time() - start)
        # TBD parse and validate the output message
        return output_message
