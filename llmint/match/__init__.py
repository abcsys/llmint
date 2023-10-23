from abc import abstractmethod
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from llmint.mint.telemetry import Telemetry

class Match():
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
            with self.telemetry.report(cb):
                output_message = self.chain.invoke(input)
        return output_message


__all__ = [
    'util',
    'record'
]
