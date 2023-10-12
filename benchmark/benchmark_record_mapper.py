import os
from benchmark import util
from benchmark.log import (
    init_logger, log_name, log, header
)

from llmint.extract import from_mint_sample
from llmint.mapper.record import RecordChatMapper
import llmint.mapper.output as output_util

__dir__ = os.path.dirname(__file__)
__log_dir__ = os.path.join(__dir__, "logs")
default_dataset = os.path.join(
    __dir__, "..", "..",
    "mint-sample-data",
    "device", "flat_light_varied_value.yaml"
)


def run(mapper, test_set):
    map_correct = []

    log("Examples:")
    log(mapper.examples)

    for i, sample in enumerate(test_set):
        log(header(f"Test {i + 1}"))
        log(header("Input"))

        source, target = sample["source"], sample["target"]
        true_mapping = sample["mapping"]
        log(mapper.format_input(source, target))

        pred_mapping = mapper.invoke(
            source_schema=source,
            target_schema=target,
        )["text"]

        # validate the prediction
        try:
            pred_mapping = output_util.format_output(pred_mapping)
        except:
            pass
        is_correct = pred_mapping == true_mapping
        map_correct.append(is_correct)

        log(header("Prediction"))
        log(f"True: {true_mapping}")
        log(f"Pred: {pred_mapping}")

        log(header("Stats"))
        log(f"{'Correct' if is_correct else 'Incorrect'}")
        if not is_correct:
            log(header("Diff"))
            log(output_util.diff_mapping(true_mapping, pred_mapping))
        log(f"Latency: {mapper.telemetry.latencies[-1]}")
        log(f"Token_count: {mapper.telemetry.total_tokens[-1]}")

    stats = {
        "map_correct": map_correct,
        **mapper.telemetry.stats(),
    }
    summary = {
        "total": len(map_correct),
        "accuracy": sum(map_correct) / len(map_correct),
        **mapper.telemetry.summary(),
    }

    log(header("Summary"))
    log(stats, pretty=True)
    log(summary, pretty=True)

    return stats, summary


def benchmark_vary_shot(
        # dataset params
        filepath=default_dataset,
        test_size=0.5,
        # match params
        model="gpt-3.5-turbo",
        temperature=0.0,
        match_method=RecordChatMapper,
        # benchmark params
        min_num_shot=1,
        max_num_shot=1,
        num_test=5,
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
    samples = list(from_mint_sample.read_mapping(data))
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
        mapper = match_method(
            examples=train_set[:num_shot],
            model=model,
            temperature=temperature,
            verbose=verbose,
        )

        # Evaluate the current shot
        stats, summary = run(mapper, test_set[:num_test])

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
