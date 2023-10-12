import time
import numpy as np
from langchain.callbacks import manager as cb_manager
from langchain.callbacks import get_openai_callback


class Telemetry:
    def __init__(self):
        self.total_tokens = []
        self.prompt_tokens = []
        self.completion_tokens = []
        self.latencies = []
        self.total_costs = []
        self._start_time = None
        self._cb = None

    def reset(self):
        """Resets the telemetry statistics."""
        self.__init__()

    def report(self, cb: cb_manager):
        """Starts the telemetry tracking."""
        self._start_time = time.time()
        self._cb = cb
        return self

    def stop(self):
        """Stops the telemetry tracking."""
        self.total_tokens.append(self._cb.total_tokens)
        self.prompt_tokens.append(self._cb.prompt_tokens)
        self.completion_tokens.append(self._cb.completion_tokens)
        self.total_costs.append(self._cb.total_cost)

        elapsed_time = time.time() - self._start_time
        self.latencies.append(elapsed_time)

    def stats(self):
        """Returns the telemetry statistics."""
        return {
            'avg_tokens': np.mean(self.total_tokens),
            'avg_prompt_tokens': np.mean(self.prompt_tokens),
            'avg_completion_tokens': np.mean(self.completion_tokens),
            'avg_cost': np.mean(self.total_costs),
            'avg_latency': np.mean(self.latencies),
            'min_latency': np.min(self.latencies),
            'max_latency': np.max(self.latencies),
            'min_tokens': np.min(self.total_tokens),
            'max_tokens': np.max(self.total_tokens),
            'total_tokens': np.sum(self.total_tokens),
            'total_costs': np.sum(self.total_costs),
        }

    def __enter__(self):
        """Enter the telemetry tracking context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the telemetry tracking context."""
        self.stop()


def test():
    from langchain.llms import OpenAI
    from llmint import util
    import pprint as pp

    llm = OpenAI(openai_api_key=util.get_openai_key())

    telemetry = Telemetry()
    with get_openai_callback() as cb:
        with telemetry.report(cb):
            print(llm("Hello!", temperature=0.1))

    pp.pprint(telemetry.stats())


if __name__ == '__main__':
    test()
