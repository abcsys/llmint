import os
from benchmark import util
from benchmark.util import header
import numpy as np
import pprint as pp

from llmint.extract import from_mint_sample
from llmint.match.record import RecordChatMatch

__dir__ = os.path.dirname(__file__)
default_dataset = os.path.join(
    __dir__, "..", "..",
    "mint-sample-data",
    "device", "flat_light.yaml"
)


def format_output(prediction):
    """Convert the prediction format to match the desired ground-truth format."""
    formatted_predictions = []
    for i in range(0, len(prediction), 3):
        entry = {
            pred.split(": ")[0].replace("'", "").strip(): pred.split(": ")[1].replace("'", "").strip()
            for pred in prediction[i:i + 3]
        }
        formatted_predictions.append(entry)
    return formatted_predictions


def run(match, test_set):
    match_correct = []

    print("Examples:")
    print(match.examples)

    for i, sample in enumerate(test_set):
        header(f"Test {i + 1}")
        header("Input")

        source, target = sample["source"], sample["target"]
        true_corresp = sample["correspondence"]
        print(match.format_input(source, target))

        pred_corresp = match.invoke(
            source_schema=source,
            target_schema=target,
        )["text"]

        # validate the prediction
        try:
            pred_corresp = format_output(pred_corresp)
        except:
            pass
        is_correct = pred_corresp == true_corresp
        match_correct.append(is_correct)

        header("Prediction")
        print(f"True: ", true_corresp)
        print(f"Pred: ", pred_corresp)

        header("Stats")
        print(f"{'Correct' if is_correct else 'Incorrect'}")
        print(f"Latency: {match.latencies[-1]}")
        print(f"Token_count: {match.token_counts[-1]}")

    summary = {
        "match_correct": match_correct,
        "token_counts": match.token_counts,
        "latencies": match.latencies,
    }
    stats = {
        "total": len(match_correct),
        "accuracy": sum(match_correct) / len(match_correct),
        "avg_token_count": np.mean(match.token_counts),
        "avg_latency": np.mean(match.latencies),
    }

    header("Summary")
    pp.pprint(summary)
    pp.pprint(stats)

    return stats, summary


def prepare_dataset(filepath, test_size):
    # Load data
    data = util.from_yaml(filepath)

    # Extract samples
    samples = list(from_mint_sample.read_corresp(data))
    train_set, test_set = util.train_test_split(samples, test_size=test_size)

    return train_set, test_set


def benchmark_vary_shot(
        # dataset params
        filepath=default_dataset,
        test_size=0.5,
        # match params
        model="gpt-3.5-turbo",
        temperature=0.0,
        match_method=RecordChatMatch,
        # benchmark params
        num_max_shot=1,
        num_test=2,
):
    """
    Run a benchmark test on a device dataset with varying shots.

    Args:
    - filepath (str): Path to the dataset file. If not provided, defaults to a specified location.
    - test_size (float): Fraction of the dataset to be used for testing.
    - num_max_shot (int): Maximum number of shots for the benchmark.
    - num_test (int): Number of test samples to use. None for using all.
    - model (str): Model name.
    - temperature (float): Sampling temperature for the model.
    - allowed_kinds (tuple): Allowed kinds of the dataset.
    - match_method (class or function): The matching method to use.

    Returns:
    - Prints the benchmark results.
    """

    # Prepare dataset
    train_set, test_set = prepare_dataset(filepath, test_size)
    assert len(test_set) > num_test, "Number of test samples is greater than the actual test set size."
    print(f"train size {len(train_set)}, test size {len(test_set)}")

    # Initialize benchmark results containers
    all_stats = {}
    token_count = 0

    # Run the benchmark
    for num_shot in range(0, num_max_shot + 1):
        header(f"Running for {num_shot} shots", char="=")

        # Initialize matching method with current shot
        match = match_method(
            examples=train_set[:num_shot],
            model=model,
            temperature=temperature,
        )

        # Evaluate the current shot
        stats, summary = run(match, test_set[:num_test])

        all_stats[num_shot] = stats
        token_count += sum(summary["token_counts"])

    # Print summary of benchmarks
    header("Benchmark summary", char="=")
    pp.pprint({
        "Accuracy": {num_shot: stats["accuracy"] for num_shot, stats in all_stats.items()},
        "Avg token count": {num_shot: stats["avg_token_count"] for num_shot, stats in all_stats.items()},
        "Avg latency": {num_shot: stats["avg_latency"] for num_shot, stats in all_stats.items()},
        "Total tokens used": token_count
    })


def main():
    benchmark_vary_shot()


if __name__ == '__main__':
    main()
