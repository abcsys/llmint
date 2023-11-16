import os
from benchmark import util
from benchmark.log import (
    init_logger, log_name, log, header
)
import numpy as np

from llmint.extract import from_mint_sample
from llmint.match.record import RecordChatMatch, RecordPromptMatch
import llmint.match.util as match_util

__dir__ = os.path.dirname(__file__)
__log_dir__ = os.path.join(__dir__, "logs")
default_dataset = os.path.join(
    __dir__, "..", "..",
    "mint-sample-data",
    "record", "flat_light.yaml" # CHANGE HERE
)
matchClass = RecordChatMatch # CHANGE HERE

"""
Benchmark script for testing accuracy, latency, and token count of RecordPromptMatch and RecordChatMatch.

Modify matchClass on line 19 to change which match class you want to test. 
Modify the yaml file name on line 17 to change which test/training example file you want to use.

The only yaml file for RecordPromptMatch is currently the record_match_prompt.yaml file. RecordChatMatch
can use any other yaml file for benchmarking.
"""

def run(match, test_set):
    match_correct = []

    log("Examples:")
    log(match.examples)

    for i, sample in enumerate(test_set):
        log(header(f"Test {i + 1}"))
        log(header("Input"))

        source, target = sample["source"], sample["target"]
        true_corresp = sample["correspondence"] if matchClass == RecordChatMatch \
                                                else match_util.pt_format_input(sample["correspondence"])
        log(match.format_input(source, target))

        pred_corresp = match.invoke(
            source_schema=source,
            target_schema=target,
        )["text"]
        
        # validate the prediction
        try:
            pred_corresp = match_util.format_output(pred_corresp) if matchClass == RecordChatMatch \
                                                                  else match_util.pt_format_output(pred_corresp)
        except:
            pass
        is_correct = pred_corresp == true_corresp
        match_correct.append(is_correct)

        log(header("Prediction"))
        log(f"True: {true_corresp}")
        log(f"Pred: {pred_corresp}")

        log(header("Stats"))
        log(f"{'Correct' if is_correct else 'Incorrect'}")
        if not is_correct:
            log(header("Diff"))
            log(match_util.diff_corresp(true_corresp, pred_corresp))
        log(f"Latency: {match.telemetry.latencies[-1]}")
        log(f"Token_count: {match.telemetry.total_tokens[-1]}")

    stats = {
        "match_correct": match_correct,
        **match.telemetry.stats(),
    }
    summary = {
        "total": len(match_correct),
        "accuracy": sum(match_correct) / len(match_correct),
        **match.telemetry.summary(),
    }

    log(header("Summary"))
    log(stats, pretty=True)
    log(summary, pretty=True)

    return stats, summary


def benchmark_vary_shot(
        # dataset params
        filepath=default_dataset,
        test_size=0.25,
        # match params
        model="gpt-3.5-turbo", # "gpt-4"
        temperature=0.0,
        match_method=matchClass,
        # benchmark params
        min_num_shot=0,
        max_num_shot=2,
        num_test=1,
        verbose=True,
        seed=42,
):
    """
    Run a benchmark test on a device dataset with varying shots.

    Args:
    - filepath (str): Path to the dataset file. If not provided, defaults to a specified location.
    - test_size (float): Fraction of the dataset to be used for testing.
    - model (str): Model name.
    - temperature (float): Sampling temperature for the model.
    - match_method (class or function): The matching method to use.
    - min_num_shot (int): Minimum number of shots for the benchmark.
    - max_num_shot (int): Maximum number of shots for the benchmark.
    - num_test (int): Number of test samples to use. None for using all.

    Returns:
    - Prints the benchmark results.
    """
    init_logger(
        log_dir=__log_dir__,
        log_file=log_name(),
        add_timestamp=True
    )
    log(f"Setup: {locals()}")

    # Prepare dataset
    data = util.from_yaml(filepath)
    # XXX detect sample type
    if (match_method == RecordChatMatch):
        samples = list(from_mint_sample.read_match(data))
    elif (match_method == RecordPromptMatch):
        samples = list(from_mint_sample.read_pt_match(data))
    train_set, test_set = util.train_test_split(samples, test_size=test_size, seed=seed)

    assert len(test_set) >= num_test, "Number of test samples is greater than the actual test set size."
    log(f"train size {len(train_set)}, test size {len(test_set)}")

    # Initialize benchmark results containers
    all_summaries = {}
    token_count = 0

    # Run the benchmark
    for num_shot in range(min_num_shot, max_num_shot + 1):
        log(header(f"Running for {num_shot} shots", char="="))

        # Initialize matching method with current shot
        match = match_method(
            examples = train_set[:num_shot],
            model=model, 
            temperature=temperature,
            verbose=verbose,
        )

        # Evaluate the current shot
        stats, summary = run(match, test_set[:num_test])

        all_summaries[num_shot] = summary
        token_count += summary["total_tokens"]

    # Print summary of benchmarks
    log(header("Benchmark summary", char="="))
    log({
        "Accuracy": {num_shot: summary["accuracy"] for num_shot, summary in all_summaries.items()},
        "Avg token count": {num_shot: summary["avg_tokens"] for num_shot, summary in all_summaries.items()},
        "Avg latency": {num_shot: summary["avg_latency"] for num_shot, summary in all_summaries.items()},
        "Total tokens used": token_count
    }, pretty=True)


def main():
    benchmark_vary_shot()


if __name__ == '__main__':
    main()
