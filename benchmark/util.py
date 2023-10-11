import yaml
import random


def train_test_split(data, test_size=0.25, seed=42):
    """
    Split the data into a train set and a test set.

    Parameters:
    - data: List of data points
    - test_size: Proportion of the data to include in the test split
    - seed: Seed for the local random number generator

    Returns:
    - Tuple of (train_set, test_set)
    """
    if not 0 <= test_size <= 1:
        raise ValueError("Test size should be between 0 and 1.")

    # Create a local instance of the random number generator
    rng = random.Random(seed)

    # Randomly shuffle the data using the local RNG
    shuffled_data = data.copy()
    rng.shuffle(shuffled_data)

    # Calculate the split index
    split_idx = int(len(shuffled_data) * (1 - test_size))

    # Split the data
    train_set = shuffled_data[:split_idx]
    test_set = shuffled_data[split_idx:]

    return train_set, test_set


def from_yaml(filepath):
    """Load a YAML file and return the data."""
    with open(filepath, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def header(content, width=50, char="-"):
    """Format a print line with consistent width and centered content."""
    padding = width - len(content)
    left_padding = padding // 2
    right_padding = padding - left_padding

    # construct the final string with the padding and content
    formatted = f"{char * left_padding}{content}{char * right_padding}"
    print()
    print(formatted)
