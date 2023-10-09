import os
from benchmark import util
import numpy as np
import pprint as pp

from llmint.extract import from_mint_sample
from llmint.match.simple import SimpleMatch

__dir__ = os.path.dirname(__file__)


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


def eval(test_set, examples=None):
    match = SimpleMatch(
        examples=examples,
    )
    match_accurate = []
    print("prompt:", match.invoke("", "", dry_run=True))
    for i, sample in enumerate(test_set[:5]):
        corresp = match.invoke(source_schema=sample["source"],
                               target_schema=sample["target"],
                               dry_run=False)["text"]
        try:
            corresp = format_output(corresp)
        except:
            pass
        print(f"#{i + 1} ground-truth:", sample["correspondence"])
        print(f"#{i + 1} prediction:", corresp)
        match_accurate.append(corresp == sample["correspondence"])
    summary = {
        "match_accurate": match_accurate,
        "token_counts": match.token_counts,
        "latencies": match.latencies,
    }
    stats = {
        "total": len(match_accurate),
        "accuracy": sum(match_accurate) / len(match_accurate),
        "avg_token_count": np.mean(match.token_counts),
        "avg_latency": np.mean(match.latencies),
    }
    pp.pprint(summary)
    pp.pprint(stats)
    return stats, summary


def run_device_flat_vary_shot():
    # Configuration
    filepath = os.path.join(__dir__, "..", "..", "mint-sample-data",
                            "device", "flat.yaml")
    allowed_kinds = {"Smart_lights"}
    test_size = 0.5
    num_max_shot = 5

    # Load data
    data = util.from_yaml(filepath)

    # Extract samples
    samples = list(from_mint_sample.read_corresp(data, allowed_kinds=allowed_kinds))
    train_set, test_set = util.train_test_split(samples, test_size=test_size)

    print(f"train size {len(train_set)}, test size {len(test_set)}")

    # Run the benchmark
    all_stats, token_count = {}, 0
    for num_shot in range(0, num_max_shot + 1):
        print(f"======Running for {num_shot} shots=======")
        stats, summary = eval(test_set, examples=train_set[:num_shot])
        all_stats[num_shot] = stats
        token_count += sum(summary["token_counts"])

    print("/n/n")
    print("======Summary=======")
    print("Accuracy:", [(num_shot, stats["accuracy"]) for num_shot, stats in all_stats.items()])
    print("Avg token count:", [(num_shot, stats["avg_token_count"]) for num_shot, stats in all_stats.items()])
    print("Avg latency:", [(num_shot, stats["avg_latency"]) for num_shot, stats in all_stats.items()])
    print(f"Used {token_count} tokens.")



def main():
    run_device_flat_vary_shot()


if __name__ == '__main__':
    main()
