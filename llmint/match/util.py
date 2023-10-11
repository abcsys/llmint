def diff_dicts(dict1, dict2):
    """Returns the difference between two dictionaries."""
    diffs = {}
    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            diffs[key] = (value, dict2.get(key))
    return diffs


def diff_lists(list1, list2):
    """Returns the difference between two lists of dictionaries."""
    diffs = []
    for d1, d2 in zip(list1, list2):
        diff = diff_dicts(d1, d2)
        if diff:
            diffs.append(diff)
    return diffs


diff_corresp = diff_lists


def format_output(raw_output):
    """Convert the prediction format to match the desired ground-truth format."""
    # Split strings by ': ' to get key-value pairs
    split_pairs = [item.split(": ")[1].strip("'") for item in raw_output]
    # Create dictionaries in pairs of two items
    return [{'from': split_pairs[i], 'to': split_pairs[i + 1]} for i in range(0, len(split_pairs), 2)]
