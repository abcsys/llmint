from abc import ABC, abstractmethod
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from llmint.mint.telemetry import Telemetry

"""
Provides base classes for LLMs used in Llmint.

TBD Common prompt optimization methods.
See: https://www.reddit.com/r/OpenAI/comments/13scry1/how_to_reduce_your_openai_costs_by_up_to_30_3/
"""


class LLM(ABC):
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
        self.telemetry = Telemetry()

    @abstractmethod
    def prepare(self) -> (LLMChain, str):
        pass

    @abstractmethod
    def format_output(self, output) -> dict:
        pass

    @abstractmethod
    def format_input(self, source, target) -> dict:
        pass

    def invoke(self, source, target):
        input = self.format_input(source, target)

        with get_openai_callback() as cb:
            with self.telemetry.report(cb):
                output_message = self.chain.invoke(input)
        if self.verbose:
            print("Raw output from LLM:")
            print(output_message)
        try:
            return self.format_output(output_message["text"])
        except:
            raise ValueError(f"Invalid output message: {output_message}")
